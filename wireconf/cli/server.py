from wireconf.internal.keys import Keys
from wireconf.internal.repository import WireguardRepository
from wireconf.internal.files import WireguardFile
from wireconf.config import exeptions
from os.path import exists as exists_file
import sqlite3
import readchar
import requests


class ServerCLI:
    wireconf_path = 'replaced.conf' #join('/', 'etc', 'wireguard', 'wg0.conf')

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__conn = connection
        self.__repository = WireguardRepository(self.__conn)
        self.__wg = WireguardFile()

    def create_server(self, address: str, port: int) -> dict[str, any]:
        public_ip: str
        try:
            server_priv_key, _, _, _ = self.__repository.get_server_keys()
            if server_priv_key:
                raise exeptions.ConfFileByWireConfExistsError()
            
            if address:
                public_ip = address
            else:
                response = requests.get('https://ifconfig.me')
                public_ip = response.text

            if exists_file(self.wireconf_path):
                responses = ('y', 'n')
                print('A non-wireconf configuration file already exists.\nDo you want to replace it? [y/n]: ')
                confirm = readchar.readchar()
                if confirm in responses:
                    if confirm == responses[1]:
                        raise exeptions.AbortExeption()
                else:
                    raise exeptions.AbortExeption()

            priv_key, pub_key = Keys.generate_keys()

            result = self.__repository.insert_server_key(priv_key, pub_key, public_ip, port)

            if not result:
                raise exeptions.ConfFileByWireConfExistsError()

            if not self.__wg.server_config_file(priv_key, port):
                raise exeptions.ConfFileByWireConfExistsError()

            return { 'success': True }
        except exeptions.ConfFileByWireConfExistsError as e:
            return { 'error': e }
        except exeptions.AbortExeption as e:
            return { 'error': e }

    def create_peer(self, name: str) -> dict[str, any]:
        try:
            server_priv_key, _, _, _ = self.__repository.get_server_keys()
            if not server_priv_key:
                raise exeptions.NoKeysFountError()

            priv_key, pub_key = Keys.generate_keys()
            result = self.__repository.insert_peer_key(name, priv_key, pub_key)

            if not result:
                raise exeptions.PeerAlredyExistsError(name)

            ip_address, _, public_key = self.__repository.get_peer_keys(name)
            self.__wg.peer_config_file(public_key, ip_address)
            return { 'success': True }
        except exeptions.NoKeysFountError as e:
            return { 'error': e }
        except exeptions.PeerAlredyExistsError as e:
            return { 'error': e }
