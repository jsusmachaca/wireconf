from wireconf.internal.repository import WireguardRepository
from wireconf.internal.files import WireguardFile
from pygments.lexers.web import JsonLexer
from pygments.lexers.text import IniLexer
from pygments import highlight
from pygments.formatters import TerminalFormatter
import sqlite3
import qrcode
import io
import json
from os.path import curdir, join


class ClientCLI:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__conn = connection
        self.__repository = WireguardRepository(self.__conn)
        self.__wg = WireguardFile()

    def create_peer(self, peer_name: str) -> dict[str, any]:
        _, address, port = self.__repository.get_server_data()

        _, server_pub_key = self.__repository.get_server_keys()
        ip_address, private_key, _ = self.__repository.get_peer_keys(peer_name)
        config = self.__wg.peer_file(peer_name, ip_address, private_key, server_pub_key, address, port)
        qr = qrcode.QRCode(box_size=1, border=1)
        qr.add_data(config)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        print(f.read())

        return { 'success': True }

    def get_peer_conf(self, peer_name: str, is_qr: bool, output: bool) -> dict[str, any]:
        conf_file = self.__wg.get_peer_file(peer_name)
        if output:
            if is_qr:
                qr = qrcode.make(conf_file)
                qr.save(join(curdir, f'{peer_name}.png'))
            else:
                self.__wg.save_peer_file(join(curdir, f'{peer_name}.conf'), conf_file)
            return { 'success': True }

        if is_qr:
            qr = qrcode.QRCode()
            qr.add_data(conf_file)
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            print(f.read())
        else:
            color_file = highlight(conf_file, IniLexer(), TerminalFormatter())
            print(color_file.strip())

        return { 'success': True }

    def get_all_peers(self) ->  dict[str, any]:
        list_peers = self.__repository.get_all_peers()

        json_peers = json.dumps(list_peers, indent=2)
        color_json = highlight(json_peers, JsonLexer(), TerminalFormatter())
        print(color_json.strip())

        return { 'success': True }
