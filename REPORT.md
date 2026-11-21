# Track A: Mininet traffic capture and flow features

Aayush Garg | ID:2023A7PS0605P | Random seed: not applicable (no randomness is used in this experiment)

## 1. Goal
To build a small virtual network in Mininet, capture packets for three traffic types (TCP, UDP, ICMP), and extract simple per-flow features that a switch could plausibly compute.

## 2. Method
- **Setup:** Windows 11 with WSL2 (Ubuntu 22.04). Mininet with an Open vSwitch bridge, one switch and three hosts (h1, h2, h3). Only h1 and h2 carried traffic.
- **Traffic (h1 to h2):** iperf3 TCP for 10 s capped at 100 Mbit/s, iperf3 UDP for 10 s at 5 Mbit/s, and 20 ICMP pings.
- **Capture:** tcpdump on h2's interface with snaplen 96, so only headers are stored.
- **Features:** a Python script (scapy, pandas) groups packets into unidirectional flows by (src, dst, sport, dport, protocol). For each flow it computes packet count, bytes, duration, mean packet size, mean inter-arrival time and packets per second.

## 3. Results

| Flow (h1 to h2) | Packets | Bytes | Duration | Mean pkt size | Mean IAT |
|---|---|---|---|---|---|
| TCP data | 2,874 | 125,192,181 | 10.13 s | 43,560 B (artifact, see 4) | 3.5 ms |
| UDP data | 4,317 | 6,370,448 | 10.04 s | 1,476 B | 2.3 ms |
| ICMP | 20 | 1,680 | 19.44 s | 84 B | 1,023 ms |

- The TCP flow works out to about 99 Mbit/s and the UDP flow to about 5.1 Mbit/s. Both match the rate limits I set, which told me the capture and the script were working.
- The three types look clearly different: TCP has the highest rate, UDP is a steady stream of large fixed-size packets, and ICMP is tiny, sparse and evenly spaced at about 1 s.
- iperf3 also opens a TCP control connection on port 5201. It appears as small extra flows (17 and 13 packets), even in the UDP capture. I treated them separately from the data flows.
- Wireshark's Conversations view of udp.pcap matched my script's counts: 4,317 packets for the UDP data flow (plus 1 reply packet), and 17 and 13 packets for the iperf3 control flow. Screenshots are in `screenshots/`. Wireshark shows slightly larger byte counts because it includes the Ethernet header, while my script uses the IP length.

## 4. Main limitation
The mean TCP packet size of 43,560 bytes is impossible for Ethernet, where packets are at most about 1,500 bytes. The most likely cause is segmentation offload (TSO/GSO): the virtual interface passes merged "super-packets" to tcpdump before they are split. This makes the TCP packet count too low and distorts packet sizes and inter-arrival times. I did not test this by disabling offload, so it is my best explanation, not a verified one.

Other limits: each result comes from a single run on one machine with no repetition, WSL2 adds timing noise, and the throughput numbers mostly reflect my rate caps, not the link's capacity.

## 5. Where I got stuck and how I fixed it
- WSL install failed with error `0x80072eff` (download reset).
- I mistyped package and service names (`openswitch-switch`, `openvswitch-witch`), so install and start failed. Fixed by copy-pasting the commands.
- I saved the script as `topo_capture,py` (a comma), so Python could not find it. Fixed with `mv`.
- The first TCP capture was 6.5 GB because Mininet links are not throttled (about 30 Gbit/s). I deleted it and recaptured with snaplen 96 and a 100 Mbit/s cap.
- Git failed with "author identity unknown", and I entered the wrong username at a push prompt. Fixed with `git config` and a GitHub personal access token.

## 6. Week 2 plan
I would add more traffic, including an attack-like flow such as a SYN flood generated with hping3, plus several benign runs. I would restrict the features to the first few packets of each flow, as a switch would see them, and test whether simple thresholds can separate the two. I would also disable offload to get true packet sizes, and repeat each run several times so I can report variation.

## 7. AI tool use
I used Claude for guidance on setup, script writing and debugging. I ran every command myself and checked the outputs.
