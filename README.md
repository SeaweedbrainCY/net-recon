# NetRecon - Discover and verify the ports exposure of your network
<p align="center">
<img src="https://github.com/SeaweedbrainCY/net-recon/actions/workflows/build_and_publish.yml/badge.svg"/>
 <img src="https://img.shields.io/github/license/seaweedbraincy/net-recon"/>
<img src="https://img.shields.io/github/v/release/seaweedbraincy/net-recon"/>
</p>

**Want to be sure you don't have any unexpected hosts or ports reachable on your network ?**


NetRecon is a simple YAML-driven network exposure checker, by checking that no **unexpected** hosts and ports are reachable — no more blind spots. 

<p align="center">
  <img src="https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/refs/heads/main/assets/NetRecon_logo.png" alt="NetRecon Logo" width="300"/>
</p>

**Table of content**
- [NetRecon](#netrecon)
  - [⭐ Features](#-features)
  - [⚠️ Ethics, Legal Considerations & Disclaimer](#-ethics-legal-considerations--disclaimer)
    - [🛑 Ethics and Legal Use](#-ethics-and-legal-use)
    - [🧾 Disclaimer](#-disclaimer)
    - [📡 Scanning Behavior](#-scanning-behavior)
    - [⚙️ Technical Note](#️technical-note)
    - [🪪 Identification and Responsibility](#-identification-and-responsibility)
  - [🚀 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [🔧 Configuration](#-configuration)
    - [Monitored Hosts](#monitored-hosts)
    - [Network Discovery](#network-discovery)
    - [Notification](#notification)
    - [Option](#option)
  - [🛠️ Contributing](#️contributing)
  - [📜 License](#license)

## ⭐ Features
- **YAML Configuration**: Define expected hosts and ports in a simple YAML file.
- **Port Scanning**: Uses Nmap for port scanning to check if unexpected ports are open.
- **Network Discovery**: Identifies hosts on the network and verify if they're already monitored.
- **Docker**: Run the tool in a Docker container for easy deployment and isolation.
- **Notification**: Get notified via Discord if any unexpected hosts or ports are reachable.

Notification example :
<p align="center">
  <img src="https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/refs/heads/main/assets/discord_notif_example.png" alt="NetRecon Logo" width="200"/>
</p>

> [!IMPORTANT]
> NetRecon is under active development. Expect breaking changes and new features in the future.

## ⚠️ Ethics, Legal Considerations & Disclaimer

### 🛑 Ethics and Legal Use
Scanning networks and hosts **without explicit permission** is almost always an **illegal act**.  
Always ensure you have **authorization** before using this tool on any network or system.

**NetRecon** is intended for **responsible, ethical use only**.

### 🧾 Disclaimer
The author and contributors of this tool are **not responsible** for any misuse, damage, or legal consequences arising from its use.  
You use this tool **at your own risk** and must ensure compliance with all applicable laws and regulations.

### 📡 Scanning Behavior
NetRecon uses [Nmap](https://nmap.org) for port scanning and network discovery.

- Scans are **aggressive by default** (fast and thorough), not designed to be stealthy.
- They may trigger firewalls or intrusion detection systems (IDS).
- Avoid scanning production or shared environments without prior coordination.

### ⚙️ Technical Note
Running large scans may generate significant network traffic.  

### 🪪 Identification and Responsibility
Scans originate from your IP. If scanning shared or production infra, notify relevant stakeholders.

## 🚀 Getting Started
### Prerequisites
- Docker installed on your machine.
- Basic knowledge of YAML and network scanning concepts.
- A Discord webhook URL for notifications (optional).

### Installation
1. Copy or download the [docker-compose.yml](https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/main/docker-compose.yml) file from the repository : 
```bash
curl -L https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/main/docker-compose.yml -o docker-compose.yml
```
> [!WARNING]
> It is **strongly recommended** to used fixed version of the image instead of `latest` tag. You can do this by replacing `image: seaweedbrain/net-recon:latest` with `image: seaweedbrain/net-recon:<version>` in the `docker-compose.yml` file.

2. Copy or download the [config.yml](https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/main/config.example.yml) file from the repository : 
```bash
curl -L https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/main/config.example.yml -o config.yml
```
3. Edit the `config.yml` file to define your expected hosts and ports.  
   See the [Configuration](#configuration) section for details. 
4. Start your NetRecon container using Docker Compose:
```bash
docker-compose up -d
```
5. Schedule scan *optional* : NetRecon doesn't embark on any scheduling. You can use your favorite scheduler (like cron) to run the container at regular intervals. For example, to run it every day at midnight, you can add the following line to your crontab:
```bash
0 0 * * * docker compose -f /path/to/docker-compose.yml up -d
```

## 🔧 Configuration
### Monitored Hosts
The `hosts` section defines the hosts you want to monitor. The goal is to define for each host, a list of ports that are expected to be open. NetRecon will scan those hosts and check if no unexpected ports are open.
|Field|Description|Mandatory|
|---|---|---|
|`hosts.[].name`|A name for the host. This is only for your reference.|**Yes**|
|`hosts.[].ip_or_hostname`|The IP or domain name of the host to scan |**Yes**|
|`hosts.[].ports`|The list of ports expected to be open for this host|**Yes**|

### Network Discovery
*This is optional*
The `network_discovery` section defines the network ranges to scan for hosts. The goal is to be sure that every hosts of the defined network are covered by NetRecon checks. Networks will ping-scanned and will check if no unexpected hosts are reachable. 
|Field|Description|Mandatory|
|---|---|---|
|`network_discovery`|List of CIDR to discover|**No**|

### Notification
*This is optional but recommended*
The `notification` section defines the notification provider to use. Currently, only Discord is supported. The goal is to be notified of the state (green or red) of each script run.
|Field|Description|Mandatory|
|---|---|---|
|`notification.discord.url`| Webhook URL of Discord integration |**No**|

### Option 
*This is optional but recommended*
The `options` section defines the options to use for your scan. 
|Field|Description|Mandatory|
|---|---|---|
|`options.parallel_scan`|Define the number of scan that will be executed in parallel. Default is 2. **Be careful, increasing this value will heavily speed up the script, but also increase the CPU usage and heavily impact the network.**|**No**|

## 🛠️ Contributing
Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

If you like this project, please consider giving it a star on GitHub! ⭐

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/main/LICENSE) file for details.