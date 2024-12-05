import sqlite3
from os.path import exists, expanduser, join
from os import mkdir
from uuid import uuid4

class VerifyDatabase:
    home = expanduser('~')
    conn = sqlite3.Connection

    def verify_or_create(self):
        db_path = join(self.home, '.wireconf', 'keys.db')
        if exists(join(self.home, '.wireconf')):
            self.conn = sqlite3.connect(db_path)
            return

        mkdir(join(self.home, '.wireconf'))

        self.conn = sqlite3.connect(db_path)
        cur = self.conn.cursor()

        try:
            cur.execute('''
                CREATE TABLE server_keys(
                    id VARCHAR(32) PRIMARY KEY,
                    server VARCHAR(30) UNIQUE,
                    private_key VARCHAR(45),
                    public_key VARCHAR(45)
                );
            ''')
            cur.execute('''
                CREATE TABLE peer_keys(
                    id VARCHAR(32) PRIMARY KEY,
                    peer VARCHAR(32),
                    private_key VARCHAR(45),
                    public_key VARCHAR(45)
                );
            ''')

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

class WireDatase:
    def __init__(self, connection: VerifyDatabase) -> None:
        connection.verify_or_create()
        self.conn = connection.conn

    def insert_server_key(self, private_key: str, public_key: str):
        radom_uuid = uuid4()
        try:
            cur = self.conn.cursor()
            cur.execute(
                'INSERT INTO server_keys(id, server, private_key, public_key) VALUES (?, "vpn_server", ?, ?);',
                [str(radom_uuid), private_key, public_key]
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Server keys alredy exists')

    def insert_peer_key(self, private_key: str, public_key: str):
        radom_uuid = uuid4()
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO peer_keys VALUES (id, private_key, public_key);',
            [str(radom_uuid), private_key, public_key]
        )
        self.conn.commit()

    def get_server_keys(self):
        cur = self.conn.cursor()
        cur.execute('SELECT private_key, public_key FROM server_keys;')
        rows = cur.fetchall()
        for row in rows:
            print(row)