from . import recon
from .config import logging,conf
from .notification import *
import os 

def main():
    """
        scan_result = {host: 
                        {ports: 
                            [
                                {number: 22, expected: True}
                            ],
                        ip: "127.0.0.1"
                        }
                    }
    """
    logging.info("Starting scanner")
    logging.info("Loading config")
    logging.info(f"Found {len(conf.hosts.host_list)} hosts to scan")
    scan_result = {} # 
    are_hosts_all_green = True
    for host in conf.hosts.host_list.keys():
        logging.info(f"Scanning host {host}")
        open_ports, ip = recon.scan_open_ports(conf.hosts.host_list[host]["ip_or_hostname"])
        for port in open_ports:
            if host not in scan_result:
                scan_result[host] = {"ports": [], "ip":ip}

            if port not in conf.hosts.host_list[host]["open_ports"]:
                scan_result[host]["ports"] += [{"number": port, "expected": False}]
                are_hosts_all_green = False
                logging.warning(f"Port {port} is open but was not expected")
            else:
                scan_result[host]["ports"] += [{"number": port, "expected": True}]
    
    if are_hosts_all_green:
        send_port_green_notification(len(scan_result.keys()))
    else:
        send_port_red_notification(scan_result)

    if len(scan_result.keys()) >= 0:
        if os.geteuid() != 0:
            logging.error(f"[FATAL] Network discovery requires root privileges. Please run the script with sudo")
            exit(1)
        logging.info("Scanning for non-declared hosts")

        scanned_ips = [scan_result[host]["ip"] for host in scan_result.keys()]
        ip_not_scanned_by_network = {}
        are_some_ip_missing = False
        for network in conf.network_discovery.networks:
            logging.info(f"Scanning network {network}")
            up_ips = recon.scan_network(network)
            ip_not_scanned_by_network[network] = []
            for ip in up_ips:
                if ip not in scanned_ips:
                    logging.info(f"Found {ip} in network {network} which has not been scanned")
                    ip_not_scanned_by_network[network].append(ip)
                    are_some_ip_missing = True
        if are_some_ip_missing:
            send_network_discovery_red_notification(ip_not_scanned_by_network)
        else:
            nb_host = 0
            for network in ip_not_scanned_by_network.keys():
                nb_host += len(ip_not_scanned_by_network[network])
            send_network_discovery_green_notification(nb_host)

        


    logging.info("Scanner finished")


if __name__ == "__main__":
    main()