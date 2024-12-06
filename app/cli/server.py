from internal.keys import Keys
from internal.repository import WireguardRepository
from internal.wireguard import Wireguard
from os.path import exists as exists_file
import sqlite3
import requests
import qrcode
import io

class ServerCli:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self.repository = WireguardRepository(self.conn)
        self.wg = Wireguard()

    def create_server(self, port: int) -> bool:
        # /etc/wireguard/wg0.conf
        if exists_file('replaced.conf'):
            responses = ('y', 'n')
            confirm = input('The configuration file already exists. \nDo you want to replace it? [y/n]: ')
            if confirm in responses:
                if confirm == responses[1]:
                    print('Aborting...')
                    return False
            else:
                print('Aborting...')
                return False

        priv_key, pub_key = Keys.generate_keys()
        result = self.repository.insert_server_key(priv_key, pub_key)

        if not result:
            return False

        server_priv_key, _ = self.repository.get_server_keys()
        if not self.wg.server_config_file(server_priv_key, port):
            return False

        return True

    def create_peer(self, name: str) -> bool:
        priv_key, pub_key = Keys.generate_keys()
        result = self.repository.insert_peer_key(name, priv_key, pub_key)

        if not result:
            return False

        ip_address, _, public_key = self.repository.get_peer_keys(name)
        self.wg.peer_config_file(public_key, ip_address)
        return True
    
    def create_client(self, name, port):
        response = requests.get('https://ifconfig.me')
        public_ip = response.text

        server_priv_key, server_pub_key = self.repository.get_server_keys()
        ip_address, private_key, public_key = self.repository.get_peer_keys(name)
        config = self.wg.client_config_file(ip_address, private_key, server_pub_key, public_ip, port)
        qr = qrcode.QRCode()
        qr.add_data(config)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        print(f.read())
        return True
