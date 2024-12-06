from cli.server import ServerCli
from config.database_config import VerifyDatabase
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
        if not server_cli.create_server(args.port):
            print('The data generated by wireconf already exists')
            return

        result = server_cli.create_peer(args.peer)
        if result.get('error'):
            print(result.get('error'))
            return

        server_cli.create_client(args.peer, args.port)
        return


    if args.command == 'peer':
        if args.add:
            result = server_cli.create_peer(args.add)
            if not result.get('error'):
                server_cli.create_client(args.add, 51820)
                print('Peer created')
            else:
                print(result.get('error'))

        if not args.add and not args.delete:
            parser.error('[-a ADD] or [-d DELETE]is required')

if __name__ == '__main__':
    main()