##########################################
################ PHASE 2 #################
##########################################
import sqlite3

class Database:
    def __init__(self, db_name="tic_tac_toe.db"):
        self.db_connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            game_type TEXT,
            game_datetime TEXT,
            board TEXT
        )
        """)
        self.db_connection.commit()

    def save_play(self, game_id, game_type, board, game_datetime):
        # print(f"{game_id}, {game_type}, {board}, {game_datetime}")
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO plays (game_id, game_type, board, game_datetime) VALUES (?, ?, ?, ?)",
                       (game_id, game_type, str(board), game_datetime))
        self.db_connection.commit()

    def list_plays(self, page=1, page_size=10):
        cursor = self.db_connection.cursor()
        cursor.execute(f"""
            select distinct game_id, game_type, game_datetime 
            from plays 
            order by game_id desc 
            limit {page_size}
            offset {(page-1)*page_size}
            """)
        return cursor.fetchall()

    def get_plays(self, game_id):
        cursor = self.db_connection.cursor()
        cursor.execute(f"""
            select board 
            from plays 
            where game_id = {game_id}
            order by id
            """)
        return cursor.fetchall()

    def get_next_game_id(self):
        cursor = self.db_connection.cursor()
        cursor.execute(f"""
            select IFNULL(MAX(game_id), 0) + 1 
            from plays 
            """)
        return cursor.fetchone()[0]

    def get_game_count(self):
        cursor = self.db_connection.cursor()
        cursor.execute(f"""
            select COUNT(*) 
            from (select distinct game_id from plays) a 
            """)
        return cursor.fetchone()[0]

    def close(self):
        self.db_connection.close()
##########################################
################ PHASE 2 #################
##########################################