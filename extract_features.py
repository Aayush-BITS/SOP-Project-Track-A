from scapy.all import rdpcap, IP, TCP, UDP, ICMP
import pandas as pd

rows = []
for name in ['tcp', 'udp', 'icmp']:
    pkts = rdpcap(f'{name}.pcap')
    flows = {}
    for p in pkts:
        if IP not in p:
            continue
        proto = 'TCP' if TCP in p else 'UDP' if UDP in p else 'ICMP' if ICMP in p else 'OTHER'
        sport = p.sport if (TCP in p or UDP in p) else 0
        dport = p.dport if (TCP in p or UDP in p) else 0
        key = (p[IP].src, p[IP].dst, sport, dport, proto)
        flows.setdefault(key, []).append((float(p.time), p[IP].len))
    for key, items in flows.items():
        times = [t for t, _ in items]
        sizes = [s for _, s in items]
        dur = times[-1] - times[0]
        iats = [b - a for a, b in zip(times, times[1:])]
        rows.append({
            'capture': name,
            'src': key[0], 'dst': key[1],
            'sport': key[2], 'dport': key[3], 'proto': key[4],
            'packets': len(items),
            'bytes': sum(sizes),
            'duration_s': round(dur, 4),
            'mean_pkt_size': round(sum(sizes) / len(sizes), 1),
            'mean_iat_ms': round(1000 * sum(iats) / len(iats), 3) if iats else 0,
            'pkts_per_s': round(len(items) / dur, 1) if dur > 0 else 0,
        })

df = pd.DataFrame(rows)
df.to_csv('flow_features.csv', index=False)
print(df.to_string())
