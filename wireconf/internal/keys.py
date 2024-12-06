from subprocess import PIPE, Popen

class Keys:
    @staticmethod
    def generate_keys() -> tuple[str, str]:
        priv_key = Popen(['wg', 'genkey'], stdout=PIPE)

        priv_key_output = priv_key.communicate()[0].decode().strip()

        pub_key = Popen(['wg', 'pubkey'], stdin=PIPE, stdout=PIPE)

        pub_key_output = pub_key.communicate(input=priv_key_output.encode())[0].decode().strip()

        return priv_key_output, pub_key_output
