from wireconf.cli import  CLI
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    init_parser = subparsers.add_parser('init', help='Initialize config files')
    init_parser.add_argument('-P', '--peer', type=str, default='default-peer')
    init_parser.add_argument('-p', '--port', type=int, default=51820)

    peer_parser = subparsers.add_parser('peer', help='Access peer settings')
    peer_parser.add_argument('-a', '--add', type=str)
    peer_parser.add_argument('-d', '--delete', type=int)
    peer_parser.add_argument('-l', '--list', action='store_true')

    group = peer_parser.add_argument_group()
    group.add_argument('-g', '--get')
    group.add_argument('-qr', action='store_true')

    args = parser.parse_args()

    if args.command == 'init':
        CLI.init(args.peer, args.port)

    if args.command == 'peer':
        CLI.add_new_peer(args.add)
        CLI.get_config_peer(args.get)
        CLI.verify_args(parser, args)
        CLI.list_all_peers(args.list)

        if args.qr:
            print(args.qr)

if __name__ == '__main__':
    main()
