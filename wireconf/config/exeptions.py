class NoKeysFountError(Exception):
    def __init__(self):
        super().__init__('No server keys found.\nPlease run wireconf init -P <name>')

class PeerAlredyExistsError(Exception):
    def __init__(self, name):
        super().__init__(f'Peer {name} alredy exists please use another')

class ConfFileByWireConfExistsError(Exception):
    def __init__(self):
        super().__init__('The data generated by wireconf already exists')

class AbortExeption(Exception):
    def __init__(self):
        super().__init__('Aborting...')

class NoAvailableIPsError(Exception):
    def __init__(self):
        super().__init__('There are no more IPs available in the allowed range')