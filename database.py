import sqlite3

class Database:
    def __init__(self, db_name="nicks.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_generated INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_nicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game TEXT,
                nickname TEXT,
                generation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_favorite BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nick_hashes (
                hash TEXT PRIMARY KEY,
                game TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id, username, first_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        self.conn.commit()
    
    def add_generated_nick(self, user_id, game, nickname, nick_hash):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO nick_hashes (hash, game)
            VALUES (?, ?)
        ''', (nick_hash, game))
        
        cursor.execute('''
            INSERT INTO generated_nicks (user_id, game, nickname)
            VALUES (?, ?, ?)
        ''', (user_id, game, nickname))
        
        cursor.execute('''
            UPDATE users SET total_generated = total_generated + 1
            WHERE user_id = ?
        ''', (user_id,))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def check_nick_exists(self, nick_hash):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM nick_hashes WHERE hash = ?', (nick_hash,))
        return cursor.fetchone() is not None
    
    def get_user_stats(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                COUNT(DISTINCT game) as games_count
            FROM generated_nicks 
            WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchone()
    
    def add_to_favorites(self, nick_id, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE generated_nicks 
            SET is_favorite = 1 
            WHERE id = ? AND user_id = ?
        ''', (nick_id, user_id))
        self.conn.commit()
    
    def get_favorites(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, game, nickname, generation_date
            FROM generated_nicks
            WHERE user_id = ? AND is_favorite = 1
            ORDER BY generation_date DESC
        ''', (user_id,))
        return cursor.fetchall()