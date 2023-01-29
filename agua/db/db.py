from typing import Optional
import psycopg2 as pg
import dotenv as env

class AguaDB:
    """A class that works with the Agua database.

    This class expects calls to conform to the schema outlined in 
    schema.ddl
    """
    connection: Optional[pg.extensions.connection]

    def __init__(self) -> None:
        """Initializes the database connection.

        This function will not return until the connection is established.
        """
        self.connection = None
    
    def connect(self) -> bool:
        """Connects to the database.
        
        Takes no arguments as connection should be pulled direclty from env variables
        to avoid leaking credentials and mistakes.
        """
        try: 
            self.connection = pg.connect(
                host=env.get("DB_HOST"),
                port=env.get("DB_PORT"),
                user=env.get("DB_USER"),
                password=env.get("DB_PASSWORD"),
                database=env.get("DB_NAME"),
                options="-c search_path=agua,public"
            )
            return True
        except pg.Error as e:
            print(e)
            return False

    def disconnect(self) -> bool:
        """Disconnects from the database.

        This function will not return until the connection is closed.
        """
        try:
            if not self.connection.closed:
                self.connection.close()
            return True
        except pg.Error as e:
            print(e)
            return False