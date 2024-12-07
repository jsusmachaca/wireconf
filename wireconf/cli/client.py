from wireconf.internal.repository import WireguardRepository
from wireconf.internal.files import WireguardFile
from wireconf.config import exeptions
import sqlite3
import requests
import qrcode
import io


class ClientCLI:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self.repository = WireguardRepository(self.conn)
        self.wg = WireguardFile()

    def create_client(self, name) -> dict[str, any]:
        try:
            server_priv_key, _, _ = self.repository.get_server_keys()
            if not server_priv_key:
                raise exeptions.NoKeysFountError()

            response = requests.get('https://ifconfig.me')
            public_ip = response.text

            _, server_pub_key, port = self.repository.get_server_keys()
            ip_address, private_key, _ = self.repository.get_peer_keys(name)
            config = self.wg.client_config_file(name, ip_address, private_key, server_pub_key, public_ip, port)
            qr = qrcode.QRCode()
            qr.add_data(config)
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            print(f.read())

            return { 'success': True }
        except exeptions.NoKeysFountError as e:
            return { 'error': e }
