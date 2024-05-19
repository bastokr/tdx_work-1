import psycopg2
import psycopg2.extras
from PyQt5.QtWidgets import QMessageBox
import logging

class Databases:
    def __init__(self, settings=None):
        self.settings = settings
        self.db = None
        self.cursor = None
        if settings:
            self.connect(settings)

    def connect(self, settings):
        try:
            logging.info(f"Attempting to connect with settings: {settings}")
            self.db = psycopg2.connect(**settings)
            self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            logging.info("Connection successful")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {str(e)}")
            self.db = None
            self.cursor = None

    def set_settings(self, settings):
        self.settings = settings
        logging.info(f"Settings set to: {settings}")
        self.connect(settings)

    def __del__(self):
        self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def execute(self, query, args=None, return_column_names=False):
        if args is None:
            args = {}
        try:
            self.check_connection()
            self.cursor.execute(query, args)
            
            if self.cursor.description:  # It's a SELECT query
                rows = self.cursor.fetchall()
                if return_column_names:
                    colnames = [desc[0] for desc in self.cursor.description]
                    return rows, colnames
                else:
                    return rows
            else:  # It's an INSERT, UPDATE, or DELETE query
                self.commit()
                return [[self.cursor.rowcount]], ['update rows']  # Return the number of rows affected
        except Exception as e:
            logging.error(f"Error executing query: {str(e)}")
            if self.db:
                self.db.rollback()  # Rollback on error to maintain data integrity
            raise  # Re-raise the exception for further handling

    def commit(self):
        if self.db:
            self.db.commit()

    def check_connection(self):
        if self.db is None or self.cursor is None or self.db.closed != 0 or self.cursor.closed:
            logging.warning("Reconnecting to the database")
            self.connect(self.settings)
