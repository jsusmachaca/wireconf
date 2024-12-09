from wireconf.config.database_config import VerifyDatabase
from wireconf.cli import ServerCLI, ClientCLI
import argparse


def main():
    vd = VerifyDatabase()
    vd.verify_or_create()
    conn = vd.connection()

    server_cli = ServerCLI(conn)
    client_cli = ClientCLI(conn)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    init_parser = subparsers.add_parser('init', help='Initialize config files')
    init_parser.add_argument('-P', '--peer', type=str, default='default-peer')
    init_parser.add_argument('-p', '--port', type=int, default=51820)

    peer_parser = subparsers.add_parser('peer', help='Initialize config files')
    peer_parser.add_argument('-a', '--add', type=str)
    peer_parser.add_argument('-g', '--get')
    peer_parser.add_argument('-d', '--delete', type=int)

    args = parser.parse_args()

    if args.command == 'init':
        server_result = server_cli.create_server(args.port)
        if server_result.get('error'):
            print(server_result.get('error'))
            return

        peer_result = server_cli.create_peer(args.peer)
        if peer_result.get('error'):
            print(peer_result.get('error'))
            return

        client_result = client_cli.create_client(args.peer)
        if client_result.get('error'):
            print(client_result.get('error'))
            return
        return

    if args.command == 'peer':
        if args.add:
            peer_result = server_cli.create_peer(args.add)
            if peer_result.get('error'):
                print(peer_result.get('error'))
                return

            client_result = client_cli.create_client(args.add)
            if client_result.get('error'):
                print(client_result.get('error'))
                return
            return

        if args.get:
            client_cli.get_config_file(args.get)
            return

        if not args.add and not args.delete and not args.get:
            parser.error('[-a ADD], [-d DELETE] or [-g GET] is required')

if __name__ == '__main__':
    main()
