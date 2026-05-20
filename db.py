import mysql.connector
from flask import current_app, g


def get_db():
    if "db" not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config["MYSQL_HOST"],
                user=current_app.config["MYSQL_USER"],
                password=current_app.config["MYSQL_PASSWORD"],
                database=current_app.config["MYSQL_DATABASE"],
                port=current_app.config["MYSQL_PORT"],
            )
        except mysql.connector.Error as exc:
            raise RuntimeError(
                "Unable to connect to MySQL. Check MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, and MYSQL_PORT."
            ) from exc
    return g.db


def query_db(query, args=None, one=False, commit=False):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, args or ())
    if commit:
        connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    rows = cursor.fetchall()
    cursor.close()
    return (rows[0] if rows else None) if one else rows


def close_db(_=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()
