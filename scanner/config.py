import yaml 
import logging

logging.basicConfig(
                format='%(asctime)s %(levelname)s %(message)s',
                level=logging.INFO,
                datefmt='%Y-%m-%dT%H:%M:%SZ%z')


class Hosts:
    required_keys = ["ip_or_hostname", "open_ports", "name"]
    host_list = {}
    def __init__(self, hosts):
        for host in hosts:
            for key in self.required_keys:
                if key not in host:
                    logging.error(f"[FATAL] Load config fail. Was expecting the key hosts.{key} for {host["name"]}")
                    exit(1)
            self.host_list[host["name"]] = {
                "open_ports": host["open_ports"],
                "ip_or_hostname": host["ip_or_hostname"]
            }



class Config:
    required_keys = ["hosts"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key {key}")
                exit(1)
        self.hosts = Hosts(data["hosts"] if data["hosts"] != None else [])

try:
    with open("./config.yml") as config_yml:
        try:
            raw_conf = yaml.safe_load(config_yml)
            conf = Config(raw_conf)
        
        except yaml.YAMLError as exc:
            raise Exception(exc)
except Exception as e :
    logging.error(f"[FATAL] API will stop now. Error while checking /api/config/config.yml, {e}")
    exit(1)


