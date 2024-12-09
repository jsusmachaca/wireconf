from os.path import expanduser, join
import pwd


class WireguardFile:
    __home = expanduser('~')
    __wireconf_path = lambda self, server_name: join('.', f'{server_name}.conf') # /etc/wireguard/name.conf
    __peer_files = join(__home, '.wireconf', 'peers') # /etc/wireguard/peers

    def __init__(self) -> None:
        pass

    def server_file(self, server_name: str, priv_key: str, port: int) -> bool:
        with open('wireconf/templates/server/server.conf') as template, \
        open(self.__wireconf_path(server_name), 'w') as interface_file:
            lines = template.readlines()
            for line in lines:
                replaced_port = line.replace('<port>', str(port))
                replaced_priv_key = replaced_port.replace('<server private key>', priv_key)
                interface_file.write(replaced_priv_key)

        return True

    def server_file_peer(self, server_name: str, pub_key: str, ip_address: str) -> bool:
        with open('wireconf/templates/server/peer.conf') as template, \
        open(self.__wireconf_path(server_name), 'a') as interface_file:
            lines = template.readlines()
            for line in lines:
                replaced_pub_key = line.replace('<client public key>', pub_key)
                replaced_ipaddress = replaced_pub_key.replace('<private ip client>', ip_address)
                interface_file.write(replaced_ipaddress)

        return True

    def peer_file(self, peer_name, priv_ip, priv_key, serv_pub_key, address, port) -> str:
        with open('wireconf/templates/client/client.conf') as template, \
        open(join(self.__peer_files, f'{peer_name}.conf'), 'w+') as client_file:
            lines = template.readlines()
            for line in lines:
                replaced_priv_ip = line.replace('<private ip client>', priv_ip)
                replaced_priv_key = replaced_priv_ip.replace('<client private key>', priv_key)
                replaced_serv_pub_key = replaced_priv_key.replace('<server public key>', serv_pub_key)
                replaced_address = replaced_serv_pub_key.replace('<server ip|host>:<port>', f'{address}:{port}')
                client_file.write(replaced_address)

            client_file.seek(0)
            return client_file.read()

    def get_number_peers(self, server_name: str) -> int:
        peer_count = 0
        with open(self.__wireconf_path(server_name)) as interface_file:
            lines = interface_file.readlines()
            for line in lines:
                if line.startswith('[Peer]'):
                    print(line)
                    peer_count += 1
            
        return peer_count

    def get_peer_file(self, peer_name: str) -> str:
        try:
            with open(join(self.__peer_files, f'{peer_name}.conf')) as client_file:
                return client_file.read()
        except FileNotFoundError:
            return ''

    def save_peer_file(self, current_path: str, data: str) -> bool:
            with open(current_path, 'w') as client_file:
                client_file.write(data)
            return True
