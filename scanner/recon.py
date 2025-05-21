import nmap3
import ipaddress
nmap = nmap3.Nmap()
hots_discovery = nmap3.NmapHostDiscovery()


def scan_open_ports(host):
    """
        open_ports = [22, 80, 443]
    """
    scan_result_raw = nmap.scan_top_ports(host, default=1000, args="-Pn")
    is_host_an_ip = True 
    host_ip = None
    try:
        ipaddress.ip_address(host)
        host_ip = host
    except ValueError:
        is_host_an_ip = False

    open_ports = []    
    for key in scan_result_raw:
        if is_host_an_ip:
            if key == host:
                ports = scan_result_raw[key]['ports']
                for port in ports:
                    if port['state'] == 'open':
                        open_ports.append(int(port['portid']))
                break
        else:
            if "hostname" in scan_result_raw[key]:
                host_ip = key
                for related_host in scan_result_raw[key]["hostname"]:
                    if related_host["name"]==host:
                        ports = scan_result_raw[key]['ports']
                        for port in ports:
                            if port['state'] == 'open':
                                open_ports.append(int(port['portid']))
                        break
    
    return open_ports, host_ip

    

def scan_network(network):
    raw_results = hots_discovery.nmap_no_portscan(network)
    up_ips = []
    for key in raw_results:
        try:
            ipaddress.ip_address(key)
            if raw_results[key]['state']['state'] == 'up':
                up_ips.append(key)
        except:
            continue
    return up_ips