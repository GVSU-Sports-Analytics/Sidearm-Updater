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
    return response.json()


def config_database(response: dict):
    db_path = os.getcwd() + "/data/gvsac.db"
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    for year in response.keys():
        cur.execute(
            f"""CREATE TABLE baseball_{year} (key TEXT, player_name TEXT);"""
        )
    return db, cur


def column_exists(cur: sqlite3.Cursor, col_name: str, tbl_name: str) -> bool:
    data = cur.execute(
        f"""SELECT name FROM PRAGMA_TABLE_INFO('{tbl_name}') where name = '{col_name}'"""
    )
    if not data.fetchall():
        return False
    return True


def add_players(cur: sqlite3.Cursor, data):
    for year, players in data.items():
        for player_name, info in players.items():
            cur.execute(
                f"""INSERT INTO baseball_{year} (key, player_name) VALUES('{info["number"]}', '{player_name.replace("'", "''")}');"""
            )
            for col, val in info.items():
                if not column_exists(cur, col, f"baseball_{year}"):
                    cur.execute(
                        f"""ALTER TABLE baseball_{year} ADD '{col}';"""
                    )
                cur.execute(
                    f"""INSERT INTO baseball_{year} ('{col}') VALUES('{val.replace("'", "''")}');"""
                )


def main():
    r = retrieve()
    db, cur = config_database(r)
    add_players(cur, r)
    db.commit()
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
