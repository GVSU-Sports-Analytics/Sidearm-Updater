import requests
import sqlite3
import json
import os
from pprint import pprint

# eventually these will be environment variables
ENDPOINT: str = "http://127.0.0.1:3000/"

REQUEST_INFO = {
    "URL": "https://gvsulakers.com",
    "SPORT": "baseball,softball"
}


def retrieve() -> dict:
    response = requests.post(
        ENDPOINT,
        json=json.dumps(REQUEST_INFO)
    )
    return response.json()


def de_tuple(tl: list):
    stuff = []
    for tup in tl:
        for thing in tup:
            stuff.append(thing)
    return stuff


def wipe(cur: sqlite3.Cursor):
    tables = de_tuple(
        cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table';"""
        ).fetchall()
    )
    for table in tables:
        cur.execute("DROP table %s;" % table.replace("-", "_"))


def config_database(response: dict):
    db_path = os.getcwd() + "/data/gvsac.db"
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    wipe(cur)
    for sport in response:
        years = response[sport].keys()
        sport = sport.replace("-", "_")
        for year in years:
            cur.execute(
                "CREATE TABLE '{}' (key TEXT, player_name TEXT);""".format(sport + "_" + year)
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
    for sport, yr in data.items():
        sport = sport.replace("-", "_")
        for year, players in yr.items():
            for player_name, info in players.items():
                cur.execute(
                    "INSERT OR IGNORE INTO {}_{} (key, player_name) VALUES(?, ?)".format(
                        sport, year),
                    (info["number"], player_name)
                )
                for col, val in info.items():
                    if not column_exists(cur=cur, col_name=col, tbl_name=f"{sport}_{year}"):
                        cur.execute(
                            f"ALTER TABLE {sport}_{year} ADD COLUMN '{col}' TEXT"
                        )
                    cur.execute(
                        f"UPDATE {sport}_{year} SET '{col}' = ? WHERE key = ?",
                        (val, info["number"])
                    )


def main():
    r = retrieve()
    pprint(r)
    db, cur = config_database(r)
    add_players(cur, r)
    db.commit()
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
