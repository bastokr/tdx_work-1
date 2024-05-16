import psycopg2
import psycopg2.extras

class Databases:
    def __init__(self, settings=None):
        self.settings = settings
        self.db = None
        self.cursor = None
        if settings:
            self.connect(settings)

    def connect(self, settings):
        try:
            print(f"Attempting to connect with settings: {settings}")
            self.db = psycopg2.connect(**settings)
            self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print("Connection successful")
        except Exception as e:
            print(f"Failed to connect to the database: {str(e)}")
            self.db = None
            self.cursor = None

    def set_settings(self, settings):
        self.settings = settings
        print(f"Settings set to: {settings}")
        self.connect(settings)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def execute(self, query, args={}):
        if not self.cursor:
            raise Exception("Database not connected execute")
        self.cursor.execute(query, args)
        rows = self.cursor.fetchall()
        return rows

    def commit(self):
        if self.db:
            self.db.commit()
    def check_connection(self):
        if self.db is None or self.cursor is None or self.db.closed or self.cursor.closed:
            print("Reconnecting to the database")
            self.connect(self.settings)