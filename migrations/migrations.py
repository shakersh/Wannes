from app.core import Constants


class Migrations():
    @staticmethod
    def handle():
        Constants.conn.execute(''' CREATE TABLE IF NOT EXISTS ALARMS
		 (id INTEGER PRIMARY KEY AUTOINCREMENT,
		 time DATETIME NOT NULL
		 );
		''')
