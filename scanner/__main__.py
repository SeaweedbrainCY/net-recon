from . import recon
from .config import logging,conf

def main():
    logging.info("Starting scanner")
    logging.info("Loading config")
    logging.info(f"Found {len(conf.hosts.host_list)} hosts to scan")
    non_expected_open_ports_by_host = {}
    for host in conf.hosts.host_list.keys():
        logging.info(f"Scanning host {host}")
        open_ports = recon.scan_open_ports(conf.hosts.host_list[host]["ip_or_hostname"])
        non_expected_open_ports = []
        for port in open_ports:
            if port not in conf.hosts.host_list[host]["open_ports"]:
                non_expected_open_ports.append(port)
                logging.warning(f"Port {port} is open but was not expected")
        if len(non_expected_open_ports) > 0:
            non_expected_open_ports_by_host[host] = non_expected_open_ports
            logging.info(f"Found {len(non_expected_open_ports)} unexpected open ports for {host}")
            
    logging.info("Scanner finished")


if __name__ == "__main__":
    main()