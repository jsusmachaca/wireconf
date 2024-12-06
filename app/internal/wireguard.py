from os.path import exists as exists_file


class Wireguard:
    def __init__(self) -> None:
        pass

    def server_config_file(self, priv_key: str, port: int) -> bool:
        with open('app/templates/server/server.conf') as file, \
            open('replaced.conf', 'w') as replaced_file:
            lines = file.readlines()
            for line in lines:
                replaced_port = line.replace('<port>', str(port))
                replaced_priv_key = replaced_port.replace('<server private key>', priv_key)
                replaced_file.write(replaced_priv_key)

        return True
  
    def peer_config_file(self, pub_key: str, ip_address: str):
        with open('replaced.conf', 'a') as file, open('app/templates/server/peer.conf') as peer_file:
            lines = peer_file.readlines()
            for line in lines:
                replaced_pub_key = line.replace('<client public key>', pub_key)
                replaced_ipaddress = replaced_pub_key.replace('<private ip client>', ip_address)
                file.write(replaced_ipaddress)

    def client_config_file(self, priv_ip, priv_key, serv_pub_key, public_ip, port) -> str:
        with open('app/templates/client/client.conf') as file, open('replaced_client.conf', 'w+') as client_file:
            lines = file.readlines()
            for line in lines:
                replaced_priv_ip = line.replace('<private ip client>', priv_ip)
                replaced_priv_key = replaced_priv_ip.replace('<client private key>', priv_key)
                replaced_serv_pub_key = replaced_priv_key.replace('<server public key>', serv_pub_key)
                replaced_address = replaced_serv_pub_key.replace('<server ip|host>:<port>', f'{public_ip}:{port}')
                client_file.write(replaced_address)

            client_file.seek(0)
            return client_file.read()
