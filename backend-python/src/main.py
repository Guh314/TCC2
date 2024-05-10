import os

import secrets
import string

from flask import Flask, request

import sqlite3

from faker import Faker

app = Flask(_name_)

fake = Faker()

def generateRandomPassword():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(12))

    return password

#Function to populate the DB
#No f string
def populate_db(conn, pessoa_num=20):
    cur = conn.cursor()

    #Insert pessoa
    id_pessoa = cur.execute("""INSERT INTO pessoa(nome, email, senha) VALUES(?, ?, ?) RETURNING id""", (fake.name(), fake.email(), generateRandomPassword())).fetchone()[0]
    conn.commit()

    #Insert canal
    id_canal = cur.execute("""INSERT INTO canal(nome, id_criador) VALUES(?, ?) RETURNING id""", (fake.name(), id_pessoa)).fetchone()[0]
    conn.commit()

    #Insert sala
    id_sala = cur.execute("""INSERT INTO sala(nome, id_lider, id_canal) VALUES(?, ?, ?) RETURNING id""", (fake.name(), id_pessoa, id_canal)).fetchone()[0]
    conn.commit()

    id_pessoa_list = []
    #Insert pessoa_sala
    for _ in range(pessoa_num):
        id_pessoa_list.append(cur.execute("""INSERT INTO pessoa(nome, email, senha) VALUES(?, ?, ?) RETURNING id""", (fake.name(), fake.email(), generateRandomPassword())).fetchone()[0])
        conn.commit()

    #Insert message
    for i in range(pessoa_num):
        for _ in range(5):
            cur.execute("""INSERT INTO message(text, id_pessoa, id_sala) VALUES(?, ?, ?)""", (fake.sentence(), id_pessoa_list[i], id_sala))
            conn.commit()
        


#Create the Tables
def create_tables(cur):
    cur.execute("""CREATE TABLE pessoa(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT)""")
    
    cur.execute("""CREATE TABLE canal(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT, 
        id_criador INTEGER NOT NULL REFERENCES pessoa (id))""")
    
    cur.execute("""CREATE TABLE sala(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT, 
        id_lider INTEGER NOT NULL REFERENCES pessoa (id),
        id_canal INTEGER NOT NULL REFERENCES canal (id))""")
    
    cur.execute("""CREATE TABLE pessoa_sala(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        id_sala INTEGER NOT NULL REFERENCES sala (id),
        id_pessoa INTEGER NOT NULL REFERENCES pessoa (id))""")
    
    cur.execute("""CREATE TABLE message(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        text TEXT, 
        id_pessoa INTEGER NOT NULL REFERENCES pessoa (id),
        id_sala INTEGER NOT NULL REFERENCES sala (id))""")


#SQLite3 requires a new connection per context, thread
def create_conn():
    return sqlite3.connect(os.path.join("db", "rooms.db"))


if os.path.exists(os.path.join("db", "rooms.db")):
    conn = create_conn()

else:
    os.mkdir(os.path.join("db"))
    conn = create_conn()
    create_tables(conn.cursor())


#Generic cursor for testing if the DB is loaded
cur = conn.cursor()
res = cur.execute("SELECT nome FROM pessoa")

#Extend it to cover empty DB, the tables are there but they are empty
if res.fetchall() == []:
    populate_db(create_conn())

else:
    pass

#print(cur.execute("SELECT * FROM message").fetchall())

#Test the connection in get method
@app.get("/")
def get_all():
    res = create_conn()
    return res.execute("SELECT * FROM message").fetchall()


#Convert the parameter to string
@app.route("/rooms/<int:id_sala>", methods=('GET', 'POST'))
def room_msg(id_sala):
    if request.method == 'POST':
        pass

    if request.method == 'GET':
        res = create_conn()
        return res.execute("SELECT text, id_pessoa FROM message WHERE id_sala = ?", (str(id_sala))).fetchall()

    return


@app.route("/login", methods=('GET', 'POST'))
def login():
    #Create new user
    if request.method == 'POST':
        pass

    #Login
    if request.method == 'GET':
        pass

    return
