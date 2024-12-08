import sqlite3
from uuid import uuid4
from wireconf.config import exeptions


class WireguardRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection

    def insert_server_key(self, private_key: str, public_key: str, port: int):
        random_uuid = uuid4()
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT INTO server(id, server, private_key, public_key, port) VALUES (?, "vpn_server", ?, ?, ?);',
                [str(random_uuid), private_key, public_key, port]
            )
            self.conn.commit()

            return True
        except sqlite3.IntegrityError:
            return False

    def insert_peer_key(self, name: str, private_key: str, public_key: str):
        random_uuid = uuid4()
        ip_address = self.get_avialable_ip()

        cur = self.conn.cursor()
        try:
            cur.execute(
                'INSERT INTO peers(id, name, ip_address, private_key, public_key) VALUES (?, ?, ?, ?, ?);',
                [str(random_uuid), name, ip_address, private_key, public_key]
            )
            self.conn.commit()

            return True
        except sqlite3.IntegrityError as e:
            return False

    def get_server_keys(self):
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT private_key, public_key, port FROM server;')
            row = cur.fetchone()

            return row
        except Exception as e:
            return '', '', ''

    def get_peer_keys(self, name: str):
        try:
            cur = self.conn.cursor()
            cur.execute(
                'SELECT ip_address, private_key, public_key FROM peers WHERE name=?;',
                [name]
            )

            row = cur.fetchone()

            return row
        except Exception as e:
            return '', '', ''

    def get_number_peers(self) -> int:
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) FROM peers;')
        count = cur.fetchone()[0]

        return int(count)

    def get_avialable_ip(self):
        used_ips = {row[0] for row in self.conn.cursor().execute('SELECT ip_address FROM peers').fetchall()}
        for i in range(2, 255):
            candidate_ip = f'10.0.0.{i}'
            if candidate_ip not in used_ips:
                return candidate_ip
        raise exeptions.NoAvailableIPsError()
    
    def get_all_peers(self):
        cur = self.conn.cursor()
        cur.execute(
            'SELECT name, ip_addess FROM peers;'
        )
