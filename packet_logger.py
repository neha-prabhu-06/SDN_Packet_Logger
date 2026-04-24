
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, arp

log = core.getLogger()

arp_table = {}
mac_to_port = {}


def _handle_PacketIn(event):
    packet = event.parsed

    # SAFETY: ignore bad packets
    if packet is None:
        return

    dpid = event.connection.dpid

    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn MAC → port
    mac_to_port[dpid][packet.src] = event.port

    # Try to get ARP packet
    arp_pkt = packet.find('arp')

    # ======================
    # ARP HANDLING
    # ======================
    if arp_pkt is not None and arp_pkt.hwsrc is not None:
        log.info("ARP %s -> %s", arp_pkt.protosrc, arp_pkt.protodst)

        # Learn IP → MAC
        arp_table[arp_pkt.protosrc] = arp_pkt.hwsrc

        # If destination known → reply
        if arp_pkt.protodst in arp_table:
            reply = arp()
            reply.opcode = arp.REPLY
            reply.hwsrc = arp_table[arp_pkt.protodst]
            reply.hwdst = arp_pkt.hwsrc
            reply.protosrc = arp_pkt.protodst
            reply.protodst = arp_pkt.protosrc

            eth = ethernet()
            eth.type = ethernet.ARP_TYPE
            eth.src = reply.hwsrc
            eth.dst = reply.hwdst
            eth.payload = reply

            msg = of.ofp_packet_out()
            msg.data = eth.pack()
            msg.actions.append(of.ofp_action_output(port=event.port))
            event.connection.send(msg)

        return   # IMPORTANT: stop here for ARP

    # ======================
    # NORMAL FORWARDING
    # ======================
    dst = packet.dst

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("ARP + Learning Switch Started")
