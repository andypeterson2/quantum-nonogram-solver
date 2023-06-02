import sqlite3
from dataclasses import dataclass
import json
from typing import List, Optional
@dataclass
class BenchmarkMetrics:
    id: int = None
    puzzle_size: str = None
    algorithm: str = None
    steps: int = None
    time: float = None
    gates: int = None
    
@dataclass
class BenchmarkSession:
    session_id: int = None
    num_boards: int = None
    puzzle_size: str = None
    algorithm: str = None

class MetricsDatabase:
    def __del__(self):
        if self.conn:
            self.conn.close()
                  
    def __init__(self, db_path):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS BenchmarkMetrics (
                    id INTEGER PRIMARY KEY,
                    puzzle_size TEXT,
                    algorithm TEXT,
                    steps INTEGER,
                    time REAL,
                    gates INTEGER
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS BenchmarkSessions (
                    session_id INTEGER PRIMARY KEY,
                    num_boards INTEGER,
                    puzzle_size TEXT,
                    algorithm TEXT
                )
            ''')
        except Exception as e:
            print(f"Failed to connect to the database due to {str(e)}")

    def create_benchmark_metrics(self, data: BenchmarkMetrics):
        query = "INSERT INTO BenchmarkMetrics (id, puzzle_size, algorithm, steps, time, gates) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (data.id, data.puzzle_size, data.algorithm, data.steps, data.time, data.gates))
        self.conn.commit()
        return data

    def update_benchmark_metrics(self, data: BenchmarkMetrics):
        query = "UPDATE BenchmarkMetrics SET puzzle_size = ?, algorithm = ?, steps = ?, time = ?, gates=? WHERE id = ?"
        self.cursor.execute(query, (data.puzzle_size, data.algorithm, data.steps, data.time, data.gates, data.id))
        self.conn.commit()

    def delete_benchmark_metrics(self, id: int):
        query = "DELETE FROM BenchmarkMetrics WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def get_benchmark_metrics(self, id: int) -> BenchmarkMetrics:
        query = "SELECT * FROM BenchmarkMetrics WHERE id = ?"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        return BenchmarkMetrics(*result) if result else None

    def create_benchmark_session(self, data: BenchmarkSession):
        query = "INSERT INTO BenchmarkSessions (session_id, num_boards, puzzle_size, algorithm) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (data.session_id, data.num_boards, data.puzzle_size, data.algorithm))
        self.conn.commit()

    def update_benchmark_session(self, data: BenchmarkSession):
        query = "UPDATE BenchmarkSessions SET num_boards = ?, puzzle_size = ?, algorithm = ? WHERE session_id = ?"
        self.cursor.execute(query, (data.num_boards, data.puzzle_size, data.algorithm, data.session_id))
        self.conn.commit()

    def delete_benchmark_session(self, session_id: int):
        query = "DELETE FROM BenchmarkSessions WHERE session_id = ?"
        self.cursor.execute(query, (session_id,))
        self.conn.commit()

    def get_benchmark_session(self, session_id: int) -> BenchmarkSession:
        query = "SELECT * FROM BenchmarkSessions WHERE session_id = ?"
        self.cursor.execute(query, (session_id,))
        result = self.cursor.fetchone()
        return BenchmarkSession(*result) if result else None

    def __del__(self):
        self.conn.close()
        
class MemoizationDB:
                  
    def __del__(self):
        if self.conn:
            self.conn.close()
            
    def __init__(self, db_path: str):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memoization (
                l INTEGER,
                d TEXT,
                result TEXT,
                PRIMARY KEY (l, d)
            )
        """)
            print(sqlite3.version)
        except Error as e:
            print(f"Failed to connect to the database due to {str(e)}")

    def get_result(self, l: int, d: List[int]) -> Optional[List[str]]:
        d_str = json.dumps(d)
        self.cursor.execute("SELECT result FROM memoization WHERE l=? AND d=?", (l, d_str))
        row = self.cursor.fetchone()
        if row is None:
            return None
        result_str = row[0]
        return json.loads(result_str)

    def store_result(self, l: int, d: List[int], result: List[str]):
        d_str, result_str = json.dumps(d), json.dumps(result)
        self.cursor.execute("INSERT INTO memoization (l, d, result) VALUES (?, ?, ?)",
                            (l, d_str, result_str))
        self.conn.commit()