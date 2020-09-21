import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("/home/aram/Desktop/links/parser.db")
        return conn
    except Error as e:
        print(e)

def create_table_links(conn):
    try:
        sql_create_links_table = """CREATE TABLE IF NOT EXISTS links(
            id integer PRIMARY KEY,
            protocol text NULL,
            path text NOT NULL,
            domain text NULL
        )
        """
        c = conn.cursor()
        c.execute(sql_create_links_table)
    except Error as e:
        print(e)

def create_link(conn,data):
    sql = """INSERT INTO links(protocol,path,domain)
            VALUES(?,?,?)"""
    c = conn.cursor()
    c.execute(sql,data)
    conn.commit()
    return c.lastrowid

def create_table_words(conn):
    try:
        sql_create_links_table = """CREATE TABLE IF NOT EXISTS words(
            id integer PRIMARY KEY,
            word text NOT NULL,
            count integer NOT NULL
        )
        """
        c = conn.cursor()
        c.execute(sql_create_links_table)
    except Error as e:
        print(e)

def create_words(conn,data):
    sql = """INSERT INTO words(word,count)
            VALUES(?,?)"""
    c = conn.cursor()
    c.execute(sql,data)
    conn.commit()
    return c.lastrowid

def select_all_links(conn):
    c = conn.cursor()
    c.execute("Select * from links")
    rows = c.fetchall()   
    for row in rows:
        print(row)

def select_all_words(conn):
    c = conn.cursor()
    c.execute("Select * from words")
    rows = c.fetchall()   
    for row in rows:
        print(row)
