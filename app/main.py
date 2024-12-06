from cli.server import ServerCli
from config.database_config import VerifyDatabase
import argparse

if __name__ == '__main__':
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
        if server_cli.create_server(args.port):
                server_cli.create_peer(args.peer)
                server_cli.create_client(args.peer, args.port)
        else:
            print('Server keys alredy exists')

    if args.command == 'peer':
        if args.add:
            if not server_cli.create_peer(args.add):
                 print(f'Peer {args.add} alredy exists please use another')
            else:
                print('Peer created')
                server_cli.create_client(args.add, 51820)

        if not args.add and not args.delete:
            parser.error('[-a ADD] or [-d DELETE]is required')
