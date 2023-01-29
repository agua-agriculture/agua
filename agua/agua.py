# Main entrypoint for Agua
from agua.db.db import AguaDB

def run():
    """Runs the Agua application."""
    # Initialize the database connection
    db = AguaDB()
    db.connect()

    print("Connected to database")