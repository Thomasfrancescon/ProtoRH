# ProtoRH

## Link
```
Endpoint : /link
Aucune information n'est requise pour la requête de l'endpoint
Le retour possible sur l'endpoint : {"message": "Hello Link!"}
le CURL : curl -X GET http://localhost:4242/link
Il est utilisé pour l'accueil des utilisateurs
```

## Create User
```
Endpoint : /user/create
Les informations requise pour la requête de l'endpoint sont email, password, firstname, lastname, birthdaydate, adress, postalcode, age, meta et role
L'un des retour possible sur l'endpoint : [6,"test@test.fr","67btghjn9388bhnk","test","test","2023-12-12","test","50369",14,{},"2023-11-07","731804532","user"]
le CURL : curl --header "Content-Type: application/json" \
  --request POST \
  --data '{         "email" : "test@test.fr",         "password" : "test",         "firstname" : "test",         "lastname" : "test",         "birthdaydate" : "2023-12-12",         "adress" : "test",         "postalcode" : "50369",         "age" : 14,         "meta" : "{}",         "role" : "user"     }' \
 http://localhost:4242/user/create
Il est utilisé pour créer un nouvel utilisateur et crypter son mot de passe
```

## Connect
```
Endpoint : /connect
Les informations requise pour la requête de l'endpoint sont email et password
L'un des retour possible sur l'endpoint : {"message":"vous etes connecté","token":4174373036}
le CURL : curl -X POST http://localhost:4242/connect -H "Content-Type: application/json" -d '{
  "email": "machin@gmail.com",
  "password": "Thomas"
}' <br>
Il est utilisé se connecter a son compte grâce à la base de donnée
```

## Recovery User
```
Endpoint : /user/{id_user}
L'information requise pour la requête de l'endpoint est id de user qui est dans l'url
L'un des retour possible sur l'endpoint : [4,"test@test.fr","test","test","2023-12-12","test","50369",14,{},"2023-11-02","test","admin"]
le CURL : curl -X GET http://localhost:4242/user/4
Il est utilisé pour récupérer toutes les informations de l'utilisateur ciblé sauf le mot de passe pour l'administrateur et toutes les information de l'utilisateur ciblé sauf le mot de passe, l'anniversaire, address, postal_code, meta, token
```

## Update User
```
Endpoint : /user/update
L'information requise pour la requête de l'endpoint sont id, email, firstname (si admin), lastname (si admin), birthdaydate, adress, postalcode, age, meta et role (si admin)
L'un des retour possible sur l'endpoint : [4,"test@test.fr","password","test","test","2023-12-12","test","50369",14,{},"2023-11-02","test","admin"]
le CURL : curl --header "Content-Type: application/json" \
  --request POST \
  --data '{         "id" : 4, 	"email" : "test@test.fr",         "firstname" : "test",         "lastname" : "test",         "birthdaydate" : "2023-12-12",         "adress" : "test",         "postalcode" : "50369",         "age" : 14,         "meta" : "{}",         "role" : "admin"     }' \
 http://localhost:4242/user/update
Il est utilisé pour modifier toutes les information de utilisateur ciblé sauf le mot de passe et le token pour l'administrateur et toutes les information de utilisateur ciblé sauf le mot de passe, le nom, le prénom, le role et le token
```

## Update Password
```
Endpoint : /user/password
L'information requise pour la requête de l'endpoint sont email, password, new_password, repeat_new_password
L'un des retour possible sur l'endpoint : [5,"test@test.fr","password","test","test","2023-12-12","test","50369",14,{},"2023-11-02","test","user"]
le CURL : curl --header "Content-Type: application/json" \
  --request POST \
  --data '{         "email" : "test@test.fr",         "password" : "password", 	"new_password" : "password", 	"repeat_new_password" : "password" }' \
 http://localhost:4242/user/password
Il est utilisé pour modifier l'ancien mot de passe et le remplacer par le nouveau
```
