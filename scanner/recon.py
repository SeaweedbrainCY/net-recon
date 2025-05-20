import nmap3
import ipaddress
nmap = nmap3.Nmap()


def scan_open_ports(host):
    scan_result_raw = nmap.scan_top_ports(host, default=1000, args="-Pn")
    is_host_an_ip = True 
    try:
        ipaddress.ip_address(host)
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
                for related_host in scan_result_raw[key]["hostname"]:
                    if related_host["name"]==host:
                        ports = scan_result_raw[key]['ports']
                        for port in ports:
                            if port['state'] == 'open':
                                open_ports.append(int(port['portid']))
                        break
    
    return open_ports

    