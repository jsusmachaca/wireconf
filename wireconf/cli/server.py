from wireconf.internal.cmd import CMD
from wireconf.internal.repository import WireguardRepository
from wireconf.internal.files import WireguardFile
import sqlite3
import requests


class ServerCLI:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__conn = connection
        self.__repository = WireguardRepository(self.__conn)
        self.__wg = WireguardFile()

    def create_server(self, server_name: str, address: str, port: int) -> dict[str, any]:
        public_ip: str
        if address:
            public_ip = address
        else:
            response = requests.get('https://ifconfig.me')
            public_ip = response.text

        priv_key, pub_key = CMD.generate_keys()

        self.__repository.insert_server_key(server_name, priv_key, pub_key, public_ip, port)
        self.__wg.server_file(server_name, priv_key, port)

        return { 'success': True }

    def add_peer_in_server(self, peer_name: str) -> dict[str, any]:
        server_name, _, _ = self.__repository.get_server_data()

        priv_key, pub_key = CMD.generate_keys()
        self.__repository.insert_peer_key(peer_name, priv_key, pub_key)

        ip_address, _, public_key = self.__repository.get_peer_keys(peer_name)
        self.__wg.server_file_peer(server_name, public_key, ip_address)
        return { 'success': True }
