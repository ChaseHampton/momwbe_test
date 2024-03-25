from datetime import datetime, timezone
import os
import sqlite3
from pymongo import MongoClient
from scrapy.utils.project import data_path


class Db:
    def __init__(self):
        self.conn = sqlite3.connect(data_path("searches.db"))
        self.muri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["spider_runs"]

    def create_table(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, business TEXT UNIQUE, searched BOOLEAN DEFAULT 0)"
        )
        self.conn.commit()

    def lookup_id(self, bname: str) -> int:
        c = self.conn.execute("SELECT id FROM searches WHERE business = ?", (bname,))
        id = c.fetchone()
        if id:
            id = id[0]
        else:
            id = None
        c.close()
        return id

    def insert_search(self, bname: str) -> int:
        c = self.conn.execute(
            "INSERT OR IGNORE INTO searches (business) VALUES (?) RETURNING id",
            (bname,),
        )
        id = c.fetchone()
        if id:
            id = id[0]
        c.close()
        self.conn.commit()
        return id

    def mark_searched(self, id: int):
        self.conn.execute("UPDATE searches SET searched = 1 WHERE id = ?", (id,))
        self.conn.commit()

    def drop_table(self):
        self.conn.execute("DROP TABLE IF EXISTS searches")
        self.conn.commit()

    def _get_run_id(self):
        old_id = list(
            self.db["runs"].aggregate([{"$sort": {"run_id": -1}}, {"$limit": 1}])
        )
        if old_id:
            return old_id[0]["run_id"]
        else:
            return 0

    def log_run(self) -> int:
        run_id = self._get_run_id() + 1
        run_entry = {
            "run_id": run_id,
            "run_start": datetime.now(tz=timezone.utc),
            "run_by": os.environ.get("USER"),
        }
        self.db["runs"].insert_one(run_entry)
        return run_id
