from wireconf.cli import  CLI
import argparse


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    init_parser = subparsers.add_parser('init', help='Initialize config files')
    init_parser.add_argument('-n', '--name', default='wg0')
    init_parser.add_argument('--peer', type=str, default='default-peer')
    init_parser.add_argument('-addr', '--address')
    init_parser.add_argument('-p', '--port', type=int, default=51820)

    peer_parser = subparsers.add_parser('peer', help='Access peer settings')
    peer_parser.add_argument('-a', '--add', type=str)
    peer_parser.add_argument('-d', '--delete', type=int)
    peer_parser.add_argument('-l', '--list', action='store_true')

    group = peer_parser.add_argument_group()
    group.add_argument('-g', '--get', type=str)
    group.add_argument('-qr', action='store_true')
    group.add_argument('-o', '--output', action='store_true')

    args = parser.parse_args()

    CLI.verify_args(parser, args)

    if args.command == 'init':
        CLI.init(args.name, args.peer, args.address, args.port)

    if args.command == 'peer':
        if args.add:
            CLI.add_new_peer(args.add)
        elif args.get:
            CLI.get_peer_conf(args.get, args.qr, args.output)
        elif args.list:
            CLI.list_all_peers(args.list)

if __name__ == '__main__':
    main()
