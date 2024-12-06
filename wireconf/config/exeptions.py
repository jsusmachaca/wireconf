class NoKeysFountError(Exception):
    def __init__(self):
        super().__init__('No server keys found.\nPlease run wireconf init -P <name>')

class PeerAlredyExistsError(Exception):
    def __init__(self, name):
        super().__init__(f'Peer {name} alredy exists please use another')