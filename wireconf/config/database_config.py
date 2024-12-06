from os.path import expanduser, join, exists
from os import mkdir
import sqlite3

class VerifyDatabase:
    home = expanduser('~')
    db_path = join(home, '.wireconf', 'keys.db')

    def __init__(self) -> None:
        self.__conn: sqlite3.Connection

    def verify_or_create(self):
        if exists(join(self.home, '.wireconf')):
            return

        print('Generating database...')
        mkdir(join(self.home, '.wireconf'))
        mkdir(join(self.home, '.wireconf', 'config-files'))

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        try:
            cur.execute('''
                CREATE TABLE server(
                    id VARCHAR(32) PRIMARY KEY,
                    server VARCHAR(30) UNIQUE,
                    port INT,
                    private_key VARCHAR(45),
                    public_key VARCHAR(45)
                );
            ''')
            cur.execute('''
                CREATE TABLE peers(
                    id VARCHAR(32) PRIMARY KEY,
                    name VACHAR(30) UNIQUE,
                    ip_address VARCHAR(15) UNIQUE,
                    private_key VARCHAR(45),
                    public_key VARCHAR(45)
                );
            ''')

            conn.commit()
        except Exception:
            conn.rollback()

    def connection(self):
        self.__conn = sqlite3.connect(self.db_path)
        return self.__conn