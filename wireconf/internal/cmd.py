from subprocess import PIPE, Popen, run
from sqlite3 import Connection
from wireconf.internal.repository import WireguardRepository
from wireconf.config import exeptions
import sys

class CMD:
    def __init__(self, connection: Connection):
        self.__conn = connection

    @staticmethod
    def generate_keys() -> tuple[str, str]:
        priv_key = Popen(['wg', 'genkey'], stdout=PIPE)

        priv_key_output = priv_key.communicate()[0].decode().strip()

        pub_key = Popen(['wg', 'pubkey'], stdin=PIPE, stdout=PIPE)

        pub_key_output = pub_key.communicate(input=priv_key_output.encode())[0].decode().strip()

        return priv_key_output, pub_key_output

    def wg_start(self, func):
        def wrapper(*args, **kwargs):
            action = func(*args, **kwargs)
            print('Up server')
            return action
        return wrapper

    def wg_restart(self, func):
        def wrapper(*args, **kwargs):
            try:
                name = WireguardRepository.get_interface_name(self.__conn)
                if not name:
                    raise exeptions.NoKeysFountError()

                """ wg_quick_down = run(['wg-quick', 'down', name], capture_output=True)
                if wg_quick_down.returncode > 0:
                    print(wg_quick_down.stderr.decode())
                    sys.exit(1) """

                action = func(*args, **kwargs)

                """ wg_quick_up = run(['wg-quick', 'up', name], capture_output=True)
                if wg_quick_up.returncode > 0:
                    print(wg_quick_up.stderr.decode())
                    sys.exit(1) """

                return action
            except exeptions.NoKeysFountError as e:
                print(e)        
                sys.exit(1)
        return wrapper
