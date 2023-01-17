import requests
import sqlite3
import json
import os


# eventually these will be environment variables
ENDPOINT: str = "http://127.0.0.1:3000/"

REQUEST_INFO = {
    "URL": "https://gvsulakers.com"
}


def retrieve() -> dict:
    response = requests.post(
        ENDPOINT,
        json=json.dumps(REQUEST_INFO)
    )
    print(response.json())
    return response.json()


def config_database(response: requests.Response):
    db_path = os.getcwd() + "/data/gvsac.db"
    db = sqlite3.connect(db_path, check_same_thread=False)
    cur = db.cursor()
    for year in response:
        cur.execute(
            f"""CREATE TABLE baseball_{year} (id INT PRIMARY KEY, name TEXT);"""
        )
    return db, cur


def add_players(cur: sqlite3.Cursor):
    for year, players in r.RESULTS.items():
        for player_name, info in players.items():
            cur.execute(
                f"""
                    INSERT INTO baseball_{year}
                    (id, name) 
                    VALUES({int(info["number"])}, '{player_name}');
                    """
            )

            for col, val in info.items():
                cur.execute(
                    f"""
                        ALTER TABLE baseball_{year} 
                        ADD '{col}';
                        """
                )

                cur.execute(
                    f"""
                        INSERT INTO baseball_{year}
                        ('{col}') 
                        VALUES('{val}');
                        """
                )


def main():
    r = retrieve()
    db, cur = config_database(r)
    add_players(cur)
    db.commit()
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
