from discord_webhook import DiscordWebhook, DiscordEmbed
from .config import *


def send_port_green_notification(nb_hosts):
    """
    Send a notification to discord when the scan is finished and all hosts are green
    """
    for notification in conf.notification.notification_methods:
        if isinstance(notification, DiscordNotification):
            logging.info(f"Sending green notification to discord")
            webhook = DiscordWebhook(url=notification.webhook_url)
            embed = DiscordEmbed(title="🟢 NetRecon - All hosts are in green state", description=f"NetRecon scanned {nb_hosts} hosts. All hosts are compliant. Among all scanned ports, all of them are expected", color="00ff00")
            embed.set_timestamp()
            embed.set_author(
                name="NetRecon",
                icon_url="https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/refs/heads/main/assets/NetRecon_square.png",
            )

            webhook.add_embed(embed)
            webhook.execute()
            logging.info("Green notification sent to discord")

def send_port_red_notification(failing_hosts):
    """
    Send a notification to discord when the scan is finished and at least one host is red
    """
    for notification in conf.notification.notification_methods:
        if isinstance(notification, DiscordNotification):
            logging.info(f"Sending red notification to discord")
            webhook = DiscordWebhook(url=notification.webhook_url)
            host_str = "host" if len(failing_hosts.keys()) == 1 else "hosts"
            be_str = "is" if len(failing_hosts.keys()) == 1 else "are"
            embed = DiscordEmbed(title=f"🔴 NetRecon - {len(failing_hosts.keys())} {host_str} {be_str} in red state", description=f"NetRecon scanned {len(failing_hosts)} hosts. Some ports are open and shouldn't be open.", color="ff0000")
            for host in failing_hosts.keys():
                msg = ""
                for port in failing_hosts[host]['ports']:
                    if port["expected"]:
                        msg += f"🟢 {port['number']}, "
                    else:
                        msg += f"🔴 {port['number']}, "
                msg = msg[:-2]
                embed.add_embed_field(name=f"Open ports of {host} ({failing_hosts[host]['ip']}) :", value=msg, inline=False)
            embed.set_timestamp()
            embed.set_author(
                name="NetRecon",
                icon_url="https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/refs/heads/main/assets/NetRecon_square.png",
            )
            webhook.add_embed(embed)
            webhook.execute()
            logging.info("Red notification sent to discord")



def send_network_discovery_green_notification(nb_scanned):
    """
    Send a notification to discord when the scan is finished and all hosts are green
    """
    for notification in conf.notification.notification_methods:
        if isinstance(notification, DiscordNotification):
            logging.info(f"Sending network discovery green notification to discord")
            webhook = DiscordWebhook(url=notification.webhook_url)
            embed = DiscordEmbed(title="🟢 NetRecon - All hosts are monitored", description=f"NetRecon scanned {nb_scanned} hosts. All hosts are already monitored", color="00ff00")
            embed.set_timestamp()
            embed.set_author(
                name="NetRecon",
                icon_url="https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/refs/heads/main/assets/NetRecon_square.png",
            )
            webhook.add_embed(embed)
            webhook.execute()
            logging.info("Network discovery green notification sent to discord")

def send_network_discovery_red_notification(ip_not_scanned_by_network):
    """
    Send a notification to discord when the scan is finished and at least one host is red
    """
    for notification in conf.notification.notification_methods:
        if isinstance(notification, DiscordNotification):
            logging.info(f"Sending network discovery red notification to discord")
            webhook = DiscordWebhook(url=notification.webhook_url)
            embed = DiscordEmbed(title="🔴 NetRecon - Some hosts are not monitored", description=f"NetRecon scanned {len(ip_not_scanned_by_network)} network(s). Some hosts are not monitored", color="ff0000")
            for network in ip_not_scanned_by_network.keys():
                msg = ""
                for ip in ip_not_scanned_by_network[network]:
                    msg += f"🔴 {ip}, "
                msg = msg[:-2]
                embed.add_embed_field(name=f"Hosts not monitored in {network} :", value=msg, inline=False)
            embed.set_timestamp()
            embed.set_author(
                name="NetRecon",
                icon_url="https://raw.githubusercontent.com/SeaweedbrainCY/net-recon/refs/heads/main/assets/NetRecon_square.png",
            )
            webhook.add_embed(embed)
            webhook.execute()
            logging.info("Network discovery red notification sent to discord")