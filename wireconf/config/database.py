from os.path import expanduser, join, exists
from os import mkdir
import sqlite3

class VerifyDatabase:
    __home = expanduser('~')
    __db_path = join(__home, '.wireconf', 'keys.db')
    __wireconf_path = join(__home, '.wireconf')
    __config_files = join(__home, '.wireconf', 'config-files')

    def __init__(self) -> None:
        self.__conn: sqlite3.Connection

    def verify_or_create(self):
        if exists(join(self.__wireconf_path)):
            return

        print('Generating database...')
        mkdir(join(self.__wireconf_path))
        mkdir(join(self.__config_files))

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
        self.__conn = sqlite3.connect(self.db_path)
        return self.__conn