from os.path import exists as exists_file
from internal.keys import Keys
from random import randint
from os import path
from internal.db import VerifyDatabase, WireDatase


class Wireguard:
    def __init__(self) -> None:
        pass

    def server_config_file(self, priv_key: str):

        """ if exists_file('/etc/wireguard/wg0.conf'):
            print('config file alredy exists')
            return """

        with open('app/templates/server/server.conf') as file, \
            open('replaced.conf', 'w') as replaced_file:
            lines = file.readlines()
            for line in lines:
                replaced_priv_key = line.replace('<server private key>', priv_key)
                replaced_file.write(replaced_priv_key)
    
    def create_peer(self, pub_key: str):
        _, pub_key = Keys.generate_keys()
        with open('replaced.conf', 'a') as file, open('app/templates/server/peer.conf') as peer_file:
            lines = peer_file.readlines()
            for line in lines:
                replaced_pub_key = line.replace('<client public key>', pub_key)
                replaced_ipaddress = replaced_pub_key.replace('<private ip client>', f'10.0.0.{randint(2, 254)}/32')
                file.write(replaced_ipaddress)


if __name__ == '__main__':
    """ peers = 3
    wire = Wireguard()
    wire.server_config_file()
    for i in range(peers):
        wire.create_peer() """
    priv_key, pub_key = Keys.generate_keys()

    w = WireDatase(VerifyDatabase())
    w.insert_server_key(priv_key, pub_key)
    w.get_server_keys()

