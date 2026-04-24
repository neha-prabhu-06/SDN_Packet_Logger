# SDN_Packet_Logger
# 📦 Packet Logger using SDN Controller (POX + Mininet)

## 📌 Overview

This project implements a **packet logger using Software Defined Networking (SDN)**.
It uses:

* **POX Controller** → to process and log packets
* **Mininet** → to simulate a network

The controller captures packets from switches and logs key details such as:

* Source IP
* Destination IP
* Protocol

---

## 🧠 How It Works

1. A packet arrives at the switch in Mininet
2. If no rule matches, the switch sends the packet to the controller (**Packet-In**)
3. The POX controller:

   * Parses the packet
   * Extracts information
   * Logs it in real-time
4. Controller can optionally send instructions back to the switch

---

## 🏗️ Architecture

```
Hosts → Switch (OpenFlow) → POX Controller → Logger Output
```

---

## ⚙️ Requirements

* Mininet VM (recommended)
* POX Controller (pre-installed in VM)
* VirtualBox / VMware

---

## 🚀 Setup Instructions

### 1️⃣ Start Mininet VM

* Open VirtualBox
* Start Mininet VM
* Login:

```
username: mininet
password: mininet
```

---

### 2️⃣ Test Mininet

```bash
sudo mn
```

Expected:

```
mininet>
```

Exit:

```bash
exit
```

---

### 3️⃣ Run POX Controller

```bash
cd ~/pox
./pox.py forwarding.l2_learning
```

---

### 4️⃣ Run Mininet Topology

(Open new terminal)

```bash
sudo mn --topo single,3 --controller remote
```

---

### 5️⃣ Test Connectivity

```bash
pingall
```

---

## 💻 Packet Logger Implementation

### 📄 File: `packet_logger.py`

Create file:

```bash
cd ~/pox/pox/misc
nano packet_logger.py
```

### 🔧 Code

```python
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4

log = core.getLogger()

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet.parsed:
        log.warning("Incomplete packet")
        return

    ip = packet.find('ipv4')

    if ip:
        log.info("IP Packet: %s -> %s | Protocol: %s",
                 ip.srcip, ip.dstip, ip.protocol)
    else:
        log.info("Non-IP Packet")

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Packet Logger Started")
```

---

## ▶️ Run Packet Logger

```bash
cd ~/pox
./pox.py misc.packet_logger
```

---

## 📡 Generate Traffic

(Open new terminal)

```bash
sudo mn --topo single,3 --controller remote
```

Inside Mininet:

```bash
pingall
```

---

## 🎉 Output

You will see logs like:

```
IP Packet: 10.0.0.1 -> 10.0.0.2 | Protocol: 1
```

---

## 📊 Features

* Real-time packet logging
* IP-level inspection
* Protocol identification
* Works with SDN architecture

---

## 🚀 Future Enhancements

* Save logs to file (CSV/DB)
* Add GUI dashboard
* Detect network attacks (IDS)
* Filter specific traffic (TCP/UDP/ICMP)

---

## ⚠️ Notes

* Always run POX before Mininet
* Use Mininet VM to avoid Python compatibility issues
* Open multiple terminals for controller and network

---

## 👨‍💻 Author

* Your Name

---

## 📜 License

This project is for educational purposes.
