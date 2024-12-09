from os.path import expanduser, join


class WireguardFile:
    __home = expanduser('~')
    __wireconf_path = 'replaced.conf' #join('/', 'etc', 'wireguard', 'wg0.conf')

    def __init__(self) -> None:
        pass

    def server_config_file(self, priv_key: str, port: int) -> bool:
        with open('wireconf/templates/server/server.conf') as file, \
        open(self.__wireconf_path, 'w') as replaced_file:
            lines = file.readlines()
            for line in lines:
                replaced_port = line.replace('<port>', str(port))
                replaced_priv_key = replaced_port.replace('<server private key>', priv_key)
                replaced_file.write(replaced_priv_key)

        return True

    def peer_config_file(self, pub_key: str, ip_address: str) -> bool:
        with open('wireconf/templates/server/peer.conf') as peer_file, \
        open(self.__wireconf_path, 'a') as file:
            lines = peer_file.readlines()
            for line in lines:
                replaced_pub_key = line.replace('<client public key>', pub_key)
                replaced_ipaddress = replaced_pub_key.replace('<private ip client>', ip_address)
                file.write(replaced_ipaddress)
        return True

    def client_config_file(self, name, priv_ip, priv_key, serv_pub_key, public_ip, port) -> str:
        with open('wireconf/templates/client/client.conf') as file, \
        open(join(self.__home, '.wireconf', 'config-files', f'{name}.conf'), 'w+') as client_file:
            lines = file.readlines()
            for line in lines:
                replaced_priv_ip = line.replace('<private ip client>', priv_ip)
                replaced_priv_key = replaced_priv_ip.replace('<client private key>', priv_key)
                replaced_serv_pub_key = replaced_priv_key.replace('<server public key>', serv_pub_key)
                replaced_address = replaced_serv_pub_key.replace('<server ip|host>:<port>', f'{public_ip}:{port}')
                client_file.write(replaced_address)

            client_file.seek(0)
            return client_file.read()

    def get_number_peers(self) -> int:
        peer_count = 0
        with open(self.__wireconf_path) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('[Peer]'):
                    print(line)
                    peer_count += 1
            
        return peer_count

    def get_client_config_file(self, name: str) -> str:
        try:
            with open(join(self.__home, '.wireconf', 'config-files', f'{name}.conf')) as file:
                return file.read()
        except FileNotFoundError:
            return ''
    
    def write_config_file(self, current_path: str, data: str) -> bool:
            with open(current_path, 'w') as file:
                file.write(data)
            return True
