# SOP Trial Task - Track A (Mininet traffic capture and flow features)

Author: Aayush Garg | Random seed: not applicable, no randomness is used in this experiment

## Environment
Windows 11 + WSL2 (Ubuntu 22.04), Mininet, Open vSwitch, iperf3, tcpdump, Python 3 (scapy, pandas)

## Commands run
sudo apt install -y mininet openvswitch-switch iperf3 tcpdump tshark python3-pip git
pip3 install scapy pandas
sudo service openvswitch-switch start
sudo mn --test pingall
sudo mn -c
sudo python3 topo_capture.py
python3 extract_features.py | tee extract_output.txt

## Files
- topo_capture.py: 1 switch + 3 hosts, captures TCP, UDP, ICMP traffic from h1 to h2
- extract_features.py: groups packets into flows, computes features
- flow_features.csv, extract_output.txt: extracted features
- *.pcap, *.log: raw captures and iperf3/ping logs

## AI tool use
Used Claude for guidance on setup, script writing and debugging. I ran and checked all commands myself.
