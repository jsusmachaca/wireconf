from wireconf.internal.keys import Keys
from wireconf.internal.repository import WireguardRepository
from wireconf.internal.wireguard import Wireguard
from wireconf.config import exeptions
from os.path import exists as exists_file
import sqlite3
import readchar


class ServerCLI:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self.repository = WireguardRepository(self.conn)
        self.wg = Wireguard()

    def create_server(self, port: int) -> dict[str, any]:
        try:
            server_priv_key, _, _ = self.repository.get_server_keys()
            if server_priv_key:
                raise exeptions.ConfFileByWireConfExistsError()

            # /etc/wireguard/wg0.conf
            if exists_file('replaced.conf'):
                responses = ('y', 'n')
                print('A non-wireconf configuration file already exists.\nDo you want to replace it? [y/n]: ')
                confirm = readchar.readchar()
                if confirm in responses:
                    if confirm == responses[1]:
                        raise exeptions.AbortExeption()
                else:
                    raise exeptions.AbortExeption()

            priv_key, pub_key = Keys.generate_keys()
            result = self.repository.insert_server_key(priv_key, pub_key, port)

            if not result:
                raise exeptions.ConfFileByWireConfExistsError()

            if not self.wg.server_config_file(priv_key, port):
                raise exeptions.ConfFileByWireConfExistsError()

            return { 'success': True }
        except exeptions.ConfFileByWireConfExistsError as e:
            return { 'error': e }
        except exeptions.AbortExeption as e:
            return { 'error': e }

    def create_peer(self, name: str) -> dict[str, any]:
        try:
            server_priv_key, _, _ = self.repository.get_server_keys()
            if not server_priv_key:
                raise exeptions.NoKeysFountError()

            priv_key, pub_key = Keys.generate_keys()
            result = self.repository.insert_peer_key(name, priv_key, pub_key)

            if not result:
                raise exeptions.PeerAlredyExistsError(name)

            ip_address, _, public_key = self.repository.get_peer_keys(name)
            self.wg.peer_config_file(public_key, ip_address)
            return { 'success': True }
        except exeptions.NoKeysFountError as e:
            return { 'error': e }
        except exeptions.PeerAlredyExistsError as e:
            return { 'error': e }
