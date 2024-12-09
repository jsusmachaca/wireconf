from .client import ClientCLI
from .server import ServerCLI
from wireconf.config.database_config import VerifyDatabase
from argparse import ArgumentParser
import sys


class CLI:
    __vd = VerifyDatabase()
    __vd.verify_or_create()
    __conn = __vd.connection()
    __client_cli = ClientCLI(__conn)
    __server_cli = ServerCLI(__conn)

    @classmethod
    def verify_args(cls, parser: ArgumentParser, args: any) -> bool:
        args_tuple = [
            v for k, v in args._get_kwargs()
            if k not in ('list', 'qr', 'output') and k != 'command'
        ]

        if args.command == 'peer':
            if args.add and args.delete:
                parser.error('flag -d is not recognized as a -a flag')

            if args.output and not args.get:
                parser.error('flag -o cannot be used without specifying a peer -g')

            if args.qr and not args.get:
                parser.error('flag -qr cannot be used without specifying a peer -g')

            arguments = [(k, v) for k, v in vars(args).items() if k != 'command' if k != 'list']            
            if args.list:
                for arg in arguments:
                    if arg[1]:
                        parser.error(f'flag --{arg[0]} cannot be used together with -l')

            if all(arg is None for arg in args_tuple):
                parser.error('flag -a, -d or -g is required')

        return True

    @classmethod
    def init(cls, peer: str = None, port: int = None) -> bool:
        if peer is None:
            return False

        server_result = cls.__server_cli.create_server(port)
        if server_result.get('error'):
            print(server_result.get('error'))
            sys.exit(1)
            return False

        peer_result = cls.__server_cli.create_peer(peer)
        if peer_result.get('error'):
            print(peer_result.get('error'))
            sys.exit(1)
            return False

        client_result = cls.__client_cli.create_client(peer)
        if client_result.get('error'):
            print(client_result.get('error'))
            sys.exit(1)
            return False

        return True

    @classmethod
    def add_new_peer(cls, peer: str = None) -> bool:
        if peer is None:
            return False

        peer_result = cls.__server_cli.create_peer(peer)
        if peer_result.get('error'):
            print(peer_result.get('error'))
            sys.exit(1)
            return False

        client_result = cls.__client_cli.create_client(peer)
        if client_result.get('error'):
                print(client_result.get('error'))
                sys.exit(1)
                return False

        return True

    @classmethod
    def get_config_peer(cls, peer: str = None, qr: bool = False, output: bool = False) -> bool:
        if peer is None:
            return False

        result =  cls.__client_cli.get_config_file(peer, qr, output)
        if result.get('error'):
            print(result.get('error'))
            sys.exit(1)
            return False

        return True

    @classmethod
    def list_all_peers(cls, list: bool = False) -> bool:
        if list is False:
            return False

        result = cls.__client_cli.get_all_peers()
        if result.get('error'):
            print(result.get('error'))
            sys.exit(1)
            return False
