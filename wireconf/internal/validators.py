from sqlite3 import Connection
from wireconf.internal.repository import WireguardRepository
from wireconf.internal.files import WireguardFile
from wireconf.config import exeptions
from os.path import exists as exists_file
from os.path import join
from sys import exit
from readchar import readchar


class Valitador:
    __wireconf_path = lambda self, server_name: join('.', f'{server_name}.conf') # /etc/wireguard/name.conf

    def __init__(self, connection: Connection):
        self.__conn = connection
        self.__wg = WireguardFile()

    def validate_alredy_existe_file(self, func):
        def wrapper(*args, **kwargs):
            try:
                if exists_file(self.__wireconf_path(args[1])):
                    responses = ('y', 'n')
                    print('A non-wireconf configuration file already exists.\nDo you want to replace it? [y/n]: ')
                    confirm = readchar()
                    if confirm in responses:
                        if confirm == responses[1]:
                            raise exeptions.AbortExeption()
                    else:
                        raise exeptions.AbortExeption()
                return func(*args, **kwargs)
            except exeptions.AbortExeption as e:
                print(e)
                exit(1)
        return wrapper

    def validate_alredy_exists_server(self, func):     
        def wrapper(*args, **kwargs):
            try:
                name = WireguardRepository.get_interface_name(self.__conn)
                if name:
                    raise exeptions.ConfFileByWireConfExistsError()
                return func(*args, **kwargs)
            except exeptions.ConfFileByWireConfExistsError as e:
                print(e)
                exit(1)
        return wrapper

    def validate_server_keys(self, func):
        def wrapper(*args, **kwargs):
            try:
                name = WireguardRepository.get_interface_name(self.__conn)
                if not name:
                    raise exeptions.NoKeysFountError()
                return func(*args, **kwargs)
            except exeptions.NoKeysFountError as e:
                print(e)
                exit(1)
        return wrapper

    def validate_not_exists_peer(self, func):
        def wrapper(*args, **kwargs):
            try:
                file = self.__wg.get_peer_file(args[1])
                if not file:
                    raise FileNotFoundError()
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print('The peer you are trying to obtain does not exist')
                exit(1)
        return wrapper

    def validate_length_peers(self, func):
        def wrapper(*args, **kwargs):
            try:
                list_peers = WireguardRepository.list_peers(self.__conn)
                if len(list_peers) == 0:
                    raise exeptions.NoPeersToListExeption()
                return func(*args, **kwargs)
            except exeptions.NoPeersToListExeption as e:
                print(e)
                exit(1)
        return wrapper

    def validate_alredy_exists_peer(self, func):
        def wrapper(*args, **kwargs):
            try:
                peer = WireguardRepository.is_exists_peer(self.__conn, args[1])
                if peer:
                    raise exeptions.PeerAlredyExistsError(args[1])
                return func(*args, **kwargs)
            except exeptions.PeerAlredyExistsError as e:
                print(e)
                exit(1)
        return wrapper
