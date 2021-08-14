from decouple import config
import pandas as pd
import psycopg2
import psycopg2.extras as extras


class DatabaseError(psycopg2.Error):
    pass


class Database:
    """
    Database class. Handles all connections to the database on heroku.
    """
    connection = psycopg2.connect(
                                  dbname=config("DB_NAME"),
                                  port=config("DB_PORT"),
                                  host=config("DB_HOST"),
                                  user=config("DB_USER"),
                                  password=config("DB_PASSWORD")
                                  )
    connection.autocommit = True
    cursor = connection.cursor()

    def connect(self) -> object:
        """
        connects to the postgres database.
        :return: database connection cursor
        """
        try:
            return self.cursor
        except DatabaseError:
            raise DatabaseError("There was a problem connecting to the requested database.")

    def setup_table(self) -> None:
        """
        sets up the Prediction table in the database.
        :return: Table successfully created message.
        """
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Predictions(id SERIAL PRIMARY KEY, title VARCHAR,
                                                                        category VARCHAR, outputs FLOAT)""")
            print("Predictions table now available in database.")
        except (DatabaseError, Exception):
            raise DatabaseError("Could not create tables in the specified database")

    def delete_tables(self) -> None:
        """
        deletes Prediction tables from the database
        :return: Table successfully deleted message
        """
        try:
            self.cursor.execute("DROP TABLE IF EXISTS Predictions")
            print("Predictions tables no longer in database.")
        except (Exception, DatabaseError) as error:
            raise error

    def add_prediction_result_to_database(self, df: pd.DataFrame):
        """
           Adds new record to the Listings Database records.
           :param details:a dictionary that contains the title,
           category, image url, item url, price of a listing.
           :return: Record successfully added to Database message.
        """
        try:
            self.setup_table()
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % ('Predictions', cols)
            extras.execute_batch(self.cursor, query, tuples, len(df))
            print("Record successfully added to Predictions")
        except (DatabaseError, Exception) as error:
            raise error("Something went wrong when trying to add record(s)")

    def extract_predictions_from_database(self):
        try:
            self.cursor.execute("SELECT * FROM Predictions ORDER BY id DESC LIMIT 10")
            return self.cursor.fetchall()
        except Exception:
            raise Exception
