from .client import ClientCLI
from .server import ServerCLI
from wireconf.config.database_config import VerifyDatabase
from argparse import ArgumentParser


class CLI:
    __vd = VerifyDatabase()
    __vd.verify_or_create()
    __conn = __vd.connection()
    __client_cli = ClientCLI(__conn)
    __server_cli = ServerCLI(__conn)

    @classmethod
    def verify_args(cls, parser: ArgumentParser, args: any) -> bool:
        args_tuple = [arg[1] for arg in args._get_kwargs() if arg[1] != 'peer']

        if all(arg is None for arg in args_tuple):
            parser.error('[-a ADD], [-d DELETE] or [-g GET] is required')
            return False
        return True

    @classmethod
    def init(cls, peer: str = None, port: int = None) -> bool:
        if peer is None:
             return False

        server_result = cls.__server_cli.create_server(port)
        if server_result.get('error'):
            print(server_result.get('error'))
            return False

        peer_result = cls.__server_cli.create_peer(peer)
        if peer_result.get('error'):
            print(peer_result.get('error'))
            return False

        client_result = cls.__client_cli.create_client(peer)
        if client_result.get('error'):
            print(client_result.get('error'))
            return False
        return True

    @classmethod
    def add_new_peer(cls, peer: str = None) -> bool:
        if peer is None:
            return False

        peer_result = cls.__server_cli.create_peer(peer)
        if peer_result.get('error'):
            print(peer_result.get('error'))
            return False

        client_result = cls.__client_cli.create_client(peer)
        if client_result.get('error'):
                print(client_result.get('error'))
                return False
        return True

    @classmethod
    def get_config_peer(cls, peer: str = None, qr: bool = False) -> bool:
        if peer is None:
            return False

        if not peer and qr:
            print('')
            return False

        result =  cls.__client_cli.get_config_file(peer, qr)
        if result.get('error'):
            print(result.get('error'))
            return False
        return True

    @classmethod
    def list_all_peers(cls, list: bool = False) -> bool:
        if list is False:
            return False

        result = cls.__client_cli.get_all_peers()
        if result.get('error'):
            print(result.get('error'))
            return False
