devices = [
    ("192.168.1.10", [22,80,443]),
    ("192.168.1.11", [21,22,80]), 
    ("192.168.1.12", [23,80,3389])
]

risky_ports = [21, 23, 3389]

print("Scanning network devices...")

sec_risk = 0
for ip, ports in devices:
    detected_ports = []
    detected_sockets = {ip: detected_ports}

    for port in ports:
        if port in risky_ports:
            detected_ports.append(port)
            sec_risk += 1

    for riskport in detected_sockets[ip]:
        print(f"WARNING: {ip} has risky port {riskport} open!")
    
print(f"Scan complete: {sec_risk} security risks found.")