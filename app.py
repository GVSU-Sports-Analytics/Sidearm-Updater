import requests
import os


endpoint = os.getenv["SIDEARM_ENDPOINT"]

def connect_db():
    db_user = os.getenv["GVAPP_DB_USERNAME"]
    db_password = os.getenv["GVAPP_DB_PASSWORD"]
    db_host = os.getenv["GVAPP_HOST"]



def main():

    db = connect_db()
    response = requests.post(
            endpoint,
        )

    # then update the database


if __name__ == "__main__":
    main()
