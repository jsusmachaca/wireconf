import sqlite3
from uuid import uuid4
from wireconf.config import exeptions


class WireguardRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.__conn = connection

    def insert_server_key(self, server_name: str, private_key: str, public_key: str, address: str, port: int):
        random_uuid = uuid4()
        try:
            cur = self.__conn.cursor()
            cur.execute(
                'INSERT INTO server(id, name, private_key, public_key, address, port) VALUES (?, ?, ?, ?, ?, ?);',
                [str(random_uuid), server_name, private_key, public_key, address, port]
            )
            self.__conn.commit()

            return True
        except sqlite3.IntegrityError:
            return False

    def insert_peer_key(self, peer_name: str, private_key: str, public_key: str):
        random_uuid = uuid4()
        ip_address = self.get_avialable_ip()

        cur = self.__conn.cursor()
        try:
            cur.execute(
                'INSERT INTO peers(id, name, address, private_key, public_key) VALUES (?, ?, ?, ?, ?);',
                [str(random_uuid), peer_name, ip_address, private_key, public_key]
            )
            self.__conn.commit()

            return True
        except sqlite3.IntegrityError as e:
            return False

    def get_server_keys(self):
        try:
            cur = self.__conn.cursor()
            cur.execute('SELECT private_key, public_key FROM server;')
            row = cur.fetchone()
            if row is None:
                raise

            return row
        except Exception as e:
            return '', ''

    def get_server_data(self):
        try:
            cur = self.__conn.cursor()
            cur.execute('SELECT name, address, port FROM server;')
            row = cur.fetchone()
            if row is None:
                raise

            return row
        except Exception as e:
            return '', '', ''

    def get_peer_keys(self, peer_name: str):
        try:
            cur = self.__conn.cursor()
            cur.execute(
                'SELECT address, private_key, public_key FROM peers WHERE name=?;',
                [peer_name]
            )

            row = cur.fetchone()

            return row
        except Exception as e:
            return '', '', ''

    def get_number_peers(self) -> int:
        cur = self.__conn.cursor()
        cur.execute('SELECT COUNT(*) FROM peers;')
        count = cur.fetchone()[0]

        return int(count)

    def get_avialable_ip(self):
        used_ips = {row[0] for row in self.__conn.cursor().execute('SELECT address FROM peers').fetchall()}
        for i in range(2, 255):
            candidate_ip = f'10.0.0.{i}'
            if candidate_ip not in used_ips:
                return candidate_ip
        raise exeptions.NoAvailableIPsError()

    def get_all_peers(self):
        try:
            cur = self.__conn.cursor()
            cur.execute(
                'SELECT name, address FROM peers;'
            )
            peers = [
                {
                    'name': i[0],
                    'ip': i[1],
                    'config-file': f'{i[0]}.conf'
                } 
                for i in cur.fetchall()
            ]

            return peers
        except Exception as e:
            return []


    '''Static methods'''

    @staticmethod
    def get_interface_name(conn: sqlite3.Connection):
        try:
            cur = conn.cursor()
            cur.execute('SELECT name FROM server;')
            row = cur.fetchone()
            if row is None:
                raise

            return row[0]
        except Exception:
            return ''
    
    @staticmethod
    def list_peers(conn: sqlite3.Connection):
        try:
            cur = conn.cursor()
            cur.execute('SELECT name FROM peers;')
            peers = cur.fetchall()

            return peers
        except Exception as e:
            return []

    @staticmethod
    def is_exists_peer(conn: sqlite3.Connection, peer_name: str):
        try:
            cur = conn.cursor()
            cur.execute('SELECT name FROM peers WHERE name=?;', [peer_name])
            peer = cur.fetchone()
            if peer is None:
                raise
            return peer[0]
        except Exception as e:
            return ''