import subprocess, uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

import os
import hashlib

DATABASE_URL = "postgresql://jawa:ilpleut@localhost/Postgresql"

engine = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url, template="template0")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base= declarative_base()

class User(Base):
    __tablename__= "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    birthdaydate = Column(String)
    adress = Column(String)
    postalcode = Column(String)
    age = Column(Integer)
    meta = Column(String)
    registrationdate = Column(Integer)
    token = Column(String)
    role = Column(String)

class UserCreate(BaseModel):
    email : str
    password : str
    firstname : str
    lastname : str
    birthdaydate : str
    adress : str
    postalcode : str
    age : int
    meta : str
    role : str
class UserUpdate(BaseModel):
    id : int = None
    email : str
    firstname : str = None
    lastname : str = None
    birthdaydate : str
    adress : str
    postalcode : str
    age : int
    meta : str
    role : str = None

class PasswordUpdate(BaseModel):
    email : str
    password : str
    new_password : str
    repeat_new_password : str

class DepartementAdd(BaseModel):
    group : str


class ResponseModel(BaseModel):
    message: str
    token: int

class UserConnect(BaseModel):
    email : str
    password : str

app = FastAPI()


# Endpoint : /
# Type : GET
# Le Endpoint renvoie la chaine de caractère "Hello world !"
@app.get("/")
async def read_root():
    return {"message": "Hello world !"}

salt = os.urandom(16).hex()

# Endpoint : /user/create
# Type : POST
# Ce endpoint permet de creer un utilisateur crypter son password et générer un token d'utilisateur
@app.post("/user/create", response_model=tuple)
async def create_user(user : UserCreate):
    query = text('INSERT INTO "User" (email, password, firstname, lastname, birthdaydate, adress, postalcode, age, meta, registrationdate, token, role) VALUES (:email, :password, :firstname, :lastname, :birthdaydate, :adress, :postalcode, :age, :meta, CURRENT_DATE::date, :token, :role) RETURNING *')
    def hash_djb2(s):
            hash = 5381
            for x in s:
                hash = (( hash << 5) + hash) + ord(x)
            return hash & 0xFFFFFFFF
    token = hash_djb2(user.email + user.firstname + user.lastname + salt)
    str2hash = user.password + salt
    hashed_password = hashlib.md5(str2hash.encode()).hexdigest()
    values = {
        "email" : user.email,
        "password" : hashed_password,
        "firstname" : user.firstname,
        "lastname" : user.lastname,
        "birthdaydate" : user.birthdaydate,
        "adress" : user.adress,
        "postalcode" : user.postalcode,
        "age" : user.age,
        "meta" : user.meta,
        "token" : token,
        "role" : user.role
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        return result.fetchone()

# Endpoint : /connect
# Type : POST
# Le Endpoint permet de ce connecter à son compte
@app.post("/connect", response_model=ResponseModel)
async def userverif(user: UserConnect):
    session = SessionLocal()
    query = text('SELECT email, password, token FROM "User" WHERE email = :email')
    str2hash = user.password + salt
    hashed_password = hashlib.md5(str2hash.encode()).hexdigest()
    result = session.execute(query, {"email": user.email}).fetchone()
    if result is not None:
        stored_password = result[1]
        stored_token = result[2]
        if hashed_password == stored_password:
            return {"message": "vous etes connecté", "token": stored_token}
    
    raise HTTPException(status_code=400, detail="L'information n'est pas correcte.")

# Endpoint : /user/{id_user}
# Type : GET
# Le Endpoint renvoie toutes les informations de l'utilisateur ciblé sauf le mot de passe pour l'administrateur et toutes les informations de l'utilisateur ciblé sauf le mot de passe, l'anniversaire, address, postal_code, meta, token   
@app.get("/user/{id_user}")
async def recup_user (id_user : int):
    query = text('SELECT * FROM "User" WHERE id = :id_user')
    values = {
        "id_user" : id_user
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        res = result.fetchall()
        for row in res:
            if row[12] == 'user':
                return row[0],row[1],row[3],row[4],row[8],row[10],row[12]
            elif row[12] == 'admin':
                return row[0],row[1],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]
            else :
               return "Tu n'as pas les permissions pour voir ses informations là"

# Endpoint : /user/update
# Type : POST
# Le Endpoint modifier et renvoie toutes les information de utilisateur ciblé sauf le mot de passe et le token pour l'administrateur et toutes les information de utilisateur ciblé sauf le mot de passe, le nom, le prénom, le role et le token
@app.post("/user/update", response_model= tuple)
async def update_user (user :UserUpdate):
    if user.id == None:
        values = {
            "Tu n'as pas oublie l'id"
        }
        return values
    queryy = text('SELECT role FROM "User" WHERE id = :id')
    values = {
        "id" : user.id
    }
    with engine.begin() as conn:
        result = conn.execute(queryy, values)
        res = result.fetchone()
        if res[0] == 'user':
            query = text('UPDATE "User" SET email = :email, birthdaydate = :birthdaydate, adress = :adress, postalcode = :postalcode, age = :age, meta = :meta WHERE id = :id RETURNING *')
            values = {
                "id" : user.id,
                "email" : user.email,
                "birthdaydate" : user.birthdaydate,
                "adress" : user.adress,
                "postalcode" : user.postalcode,
                "age" : user.age,
                "meta" : user.meta
            }
        elif res[0] == 'admin':
            query = text('UPDATE "User" SET email = :email, firstname = :firstname, lastname = :lastname, birthdaydate = :birthdaydate, adress = :adress, postalcode = :postalcode, age = :age, meta = :meta, role = :role WHERE id = :id RETURNING *')
            values = {
                "id" : user.id,
                "email" : user.email,
                "firstname" : user.firstname,
                "lastname" : user.lastname,
                "birthdaydate" : user.birthdaydate,
                "adress" : user.adress,
                "postalcode" : user.postalcode,
                "age" : user.age,
                "meta" : user.meta,
                "role" : user.role
            }
        else :
            values = {
                "Tu n'as pas les permissions pour voir ses informations là"
            }
            return values
        with engine.begin() as conn:
                result = conn.execute(query, values)
                return result.fetchone()

# Endpoint : /user/password
# Type : POST
# Le Endpoint modifier l'ancien mot de passe pour le remplacer par le nouveau
@app.post("/user/password", response_model=tuple)
async def update_password (passw :PasswordUpdate):
    queryy = text('SELECT password FROM "User" WHERE email = :email')
    values = {
        "email" : passw.email,
        "password" : passw.password,
        "new_password" : passw.new_password ,
        "repeat_new_password" : passw.repeat_new_password
    }
    with engine.begin() as conn:
        result = conn.execute(queryy, values)
        res = result.fetchone()
        if passw.password == res[0] and passw.new_password == passw.repeat_new_password: 
            query = text('UPDATE "User" SET password = :new_password WHERE email = :email RETURNING *')
            values = {
                "email" : passw.email,
                "password" : passw.password,
                "new_password" : passw.new_password,
                "repeat_new_password" : passw.repeat_new_password
            }
            with engine.begin() as conn:
                result = conn.execute(query, values)
                return result.fetchone()
        else :
            values = {
                "L'ancien mot de passe n'est pas bon ou le nouveau a été mal écrit"
            }
            return values







# Endpoint : /picture/user/{user_id}
# Type : GET
# Le Endpoint renvoie la photo de profil de utilisateur
@app.get("/picture/user/{user_id}", response_model=tuple)
async def recup_meta (user_id : int):
    try :
        query = text('SELECT token FROM "User" WHERE id = :id')
        values = {
            "id" : user_id
        }
        with engine.begin() as conn:
            result = conn.execute(query, values)
            res = result.fetchall()
            return res[0]
    except :
        not_user = {
            type: "user_error",
            error: "User not found"
        }
        return not_user 

# Endpoint : /departements/{id_departement}/users/add
# Type : POST
# Le Endpoint va ajouter des utilisateurs dans un departement
@app.post("/departements/{id_departement}/users/add")
async def update_departement (id_departement : int, group : DepartementAdd):
    queryy = text('SELECT role FROM "User" WHERE id = :id')
    values = {
        "id" : id_departement
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        res = result.fetchone()   
    if res[0] == 'admin':
        tab = []
        query = text('SELECT name FROM department WHERE id = :id_departement')
        values = {
            "id_departement" : id_departement
        }
        with engine.begin() as conn:
            result = conn.execute(query, values)
            res = result.fetchall()
            for e in group.group :
                if e in res == False:
                    res.append(e)
                    tab.append(e)
        queryy = text('UPDATE department SET name = :name WHERE id = :id_departement')
        values = {
            "name" : res,
            "id_departement" : id_departement
        }
        with engine.begin() as conn:
            result = conn.execute(queryy, values)
            return result.fetchone() and tab
    else :
        return "Tu n'as pas la permission de faire cela"

# Endpoint : /departements/{id_departement}/users/add
# Type : POST
# Le Endpoint va retirer des utilisateurs dans un departement
@app.post("/departements/{id_departement}/users/remove")
async def update_password (id_departement : int, group : DepartementAdd):
    #if role == 'admin':
    tab = []
    query = text('SELECT name FROM department WHERE id = :id_departement')
    values = {
        "id_departement" : id_departement
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        res = result.fetchall()
        for e in group.group :
            if e in res == True:
                res.remove(e)
                tab.append(e)
    queryy = text('UPDATE department SET name = :name WHERE id = :id_departement')
    values = {
        "name" : res,
        "id_departement" : id_departement
    }
    with engine.begin() as conn:
        result = conn.execute(queryy, values)
        return result.fetchone() and tab
    #else :
        #return 'Tu n'as pas la permission de faire cela'

# Endpoint : /departements/{id_departement}/users/add
# Type : GET
# Le Endpoint renvoie toutes les information des utilisateurs du departement ciblé sauf le mot de passe pour l'administrateur et toutes les information des utilisateurs du departement ciblé sauf le mot de passe, l'anniversaire, address, postal_code, meta, token
@app.get("/departements/{id_departement}/users")
async def recup_user_departement (id_departement : int):
    query = text('SELECT name FROM department WHERE id = :id_departement')
    values = {
        "id_departement" : id_departement
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        res = result.fetchall()
        for i in range (len(res)):
            #queryy = text('SELECT * FROM "User" INNER JOIN departemnt "User".id')
            queryy = text('SELECT * FROM "User" WHERE id = i')
            values = {
                "id_departement" : id_departement
            }
            with engine.begin() as conn:
                result = conn.execute(queryy, values)
                res = result.fetchall()
                #if roles == 'user':
                for row in res:
                    return row[0],row[1],row[3],row[4],row[8],row[10],row[12]
                #elif roles == 'admin':
                #for row in res:
                #    return row[0],row[1],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]

