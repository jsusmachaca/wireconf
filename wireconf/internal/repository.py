import sqlite3
from uuid import uuid4
from random import randint


class WireguardRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection

    def insert_server_key(self, private_key: str, public_key: str):
        random_uuid = uuid4()
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT INTO server(id, server, private_key, public_key) VALUES (?, "vpn_server", ?, ?);',
                [str(random_uuid), private_key, public_key]
            )
            self.conn.commit()

            return True
        except sqlite3.IntegrityError:
            return False

    def insert_peer_key(self, name: str, private_key: str, public_key: str):
        random_uuid = uuid4()
        random_ip = f'10.0.0.{randint(2, 254)}'
        cur = self.conn.cursor()
        try:
            cur.execute(
                'INSERT INTO peers(id, name, ip_address, private_key, public_key) VALUES (?, ?, ?, ?, ?);',
                [str(random_uuid), name, random_ip, private_key, public_key]
            )
            self.conn.commit()

            return True
        except sqlite3.IntegrityError as e:
            random_ip = f'10.0.0.{randint(2, 254)}'
            if str(e).split(': ')[1] == 'peer.ip_address':
                cur.execute(
                    'INSERT INTO peers(id, name, ip_address, private_key, public_key) VALUES (?, ?, ?, ?, ?);',
                    [str(random_uuid), name, random_ip, private_key, public_key]
                )
                self.conn.commit()
                return True
            return False

    def get_server_keys(self):
        try:
            private_key: str
            public_key: str

            cur = self.conn.cursor()
            cur.execute('SELECT private_key, public_key FROM server;')
            rows = cur.fetchall()
            for row in rows:
                private_key = row[0]
                public_key = row[1]
            
            return private_key, public_key
        except Exception as e:
            return '', ''

    def get_peer_keys(self, name: str):
        private_key: str
        public_key: str
        ip_address: str

        cur = self.conn.cursor()
        cur.execute(
            'SELECT ip_address, private_key, public_key FROM peers WHERE name=?;',
            [name]
        )

        row = cur.fetchone()
        ip_address = row[0]
        private_key = row[1]
        public_key = row[2]

        return (ip_address, private_key, public_key)
    
    def get_number_peers(self) -> int:
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) FROM peers;')
        count = cur.fetchone()[0]

        return int(count)
