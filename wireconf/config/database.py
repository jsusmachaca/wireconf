from os.path import expanduser, join, exists
from os import mkdir
import sqlite3

class VerifyDatabase:
    __home = expanduser('~')
    __db_path = join(__home, '.wireconf', 'keys.db')
    __wireconf_dir = join(__home, '.wireconf')
    __peer_files = join(__home, '.wireconf', 'peers')

    def __init__(self) -> None:
        self.__conn: sqlite3.Connection

    def verify_or_create(self):
        if exists(join(self.__wireconf_dir)):
            return

        print('Generating database...')
        mkdir(join(self.__wireconf_dir))
        mkdir(join(self.__peer_files))

        conn = sqlite3.connect(self.__db_path)
        cur = conn.cursor()

        try:
            cur.execute('''
                CREATE TABLE server(
                    id VARCHAR(32) PRIMARY KEY,
                    name VARCHAR(30) UNIQUE,
                    address VARCHAR(15) UNIQUE,
                    port INT,
                    private_key VARCHAR(45),
                    public_key VARCHAR(45)
                );
            ''')
            cur.execute('''
                CREATE TABLE peers(
                    id VARCHAR(32) PRIMARY KEY,
                    name VACHAR(30) UNIQUE,
                    address VARCHAR(15) UNIQUE,
                    private_key VARCHAR(45),
                    public_key VARCHAR(45)
                );
            ''')

            conn.commit()
        except Exception:
            conn.rollback()

    def connection(self):
        self.__conn = sqlite3.connect(self.__db_path)
        return self.__conn