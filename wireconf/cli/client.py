import pygments.formatters
import pygments.lexer
import pygments.lexers
import pygments.lexers.web
from wireconf.internal.repository import WireguardRepository
from wireconf.internal.files import WireguardFile
from wireconf.config import exeptions
from pygments.lexers.web import JsonLexer
from pygments.lexers.text import IniLexer
from pygments import highlight
from pygments.formatters import TerminalFormatter
import sqlite3
import requests
import qrcode
import io
import json


class ClientCLI:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__conn = connection
        self.__repository = WireguardRepository(self.__conn)
        self.__wg = WireguardFile()

    def create_client(self, name: str) -> dict[str, any]:
        try:
            server_priv_key, _, _ = self.__repository.get_server_keys()
            if not server_priv_key:
                raise exeptions.NoKeysFountError()

            response = requests.get('https://ifconfig.me')
            public_ip = response.text

            _, server_pub_key, port = self.__repository.get_server_keys()
            ip_address, private_key, _ = self.__repository.get_peer_keys(name)
            config = self.__wg.client_config_file(name, ip_address, private_key, server_pub_key, public_ip, port)
            qr = qrcode.QRCode()
            qr.add_data(config)
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            print(f.read())

            return { 'success': True }
        except exeptions.NoKeysFountError as e:
            return { 'error': e }

    def get_config_file(self, name, is_qr) -> dict[str, any]:
        try:
            conf_file = self.__wg.get_client_config_file(name)
            if not conf_file:
                raise FileNotFoundError

            if is_qr:
                qr = qrcode.QRCode()
                qr.add_data(conf_file)
                f = io.StringIO()
                qr.print_ascii(out=f)
                f.seek(0)
                print(f.read())

                return { 'success': True }
            else:
                color_file = highlight(conf_file, IniLexer(), TerminalFormatter())
                print(color_file.strip())

                return { 'success': True }
        except FileNotFoundError:
            return { 'error': 'The peer you are trying to obtain does not exist' }

    def get_all_peers(self) ->  dict[str, any]:
        try:
            list_peers = self.__repository.get_all_peers()
            if len(list_peers) == 0:
                raise exeptions.NoPeersToListExeption()

            json_peers = json.dumps(list_peers, indent=2)
            color_json = highlight(json_peers, JsonLexer(), TerminalFormatter())
            print(color_json.strip())

            return { 'success': True }
        except exeptions.NoPeersToListExeption as e:
            return { 'error': e }
