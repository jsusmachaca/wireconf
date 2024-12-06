from wireconf.cli.server import ServerCli
from wireconf.config.database_config import VerifyDatabase
import argparse


def main():
    vd = VerifyDatabase()
    vd.verify_or_create()
    conn = vd.connection()

    server_cli = ServerCli(conn)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    init_parser = subparsers.add_parser('init', help='Initialize config files')
    init_parser.add_argument('-P', '--peer', type=str, required=True)
    init_parser.add_argument('-p', '--port', type=int, default=51820)

    peer_parser = subparsers.add_parser('peer', help='Initialize config files')
    peer_parser.add_argument('-a', '--add', type=str)
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

        client_result = server_cli.create_client(args.peer, args.port)
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

            client_result = server_cli.create_client(args.add, 51820)
            if client_result.get('error'):
                print(client_result.get('error'))
                return

            print('Peer created')
            return

        if not args.add and not args.delete:
            parser.error('[-a ADD] or [-d DELETE] is required')

if __name__ == '__main__':
    main()
