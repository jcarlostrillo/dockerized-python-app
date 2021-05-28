import psycopg2
import os

class postgress_connection():
    """postgress db connection"""
    
    def __init__(self, **params):
        """ Connect to the PostgreSQL database server """
        self.connection = None
        if (self.connection is not None):
            print("Conection was already created")
        else:
            try:
                print("Params: " + str(params))
                # read connection parameters
                USER = os.getenv('POSTGRES_USER')
                PASSWORD = os.environ.get('POSTGRES_PASSWORD')
                DATABASE = os.environ.get('POSTGRES_DB')
                HOST = os.environ.get('POSTGRES_HOST')

                # connect to the PostgreSQL server
                print('Connecting to the PostgreSQL database...')
                self.connection = psycopg2.connect(
                    host=HOST,
                    database=DATABASE,
                    user=USER,
                    password=PASSWORD)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                
    
    def insert(self, ip, path, hostname, time):
        if (self.connection is None):
            print('Connection was not created')
        else:
            # create a cursor
            cursor = self.connection.cursor()

            postgres_insert_query = """ INSERT INTO requests (ip, path, host, requested_at) VALUES (%s,%s,%s, %s)"""
            record_to_insert = (ip, path, hostname, time)
            cursor.execute(postgres_insert_query, record_to_insert)

            self.connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into requests table")

    def selectAll(self):
        if (self.connection is None):
            print('Connection was not created')
        else:
            cursor = self.connection.cursor()
            postgreSQL_select_Query = "SELECT * from requests"

            cursor.execute(postgreSQL_select_Query)
            print("Selecting rows from requests table using cursor.fetchall")
            request_records = cursor.fetchall()
            return request_records
    
    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print('Database connection closed.')
        else:
            print('Connection was already closed.')
        