
# Api para softorders




## Instalacion

Instalacion del proyecto

```bash
  py -3 -m venv .venv
  pip install -r requirements.txt
```
    
## Uso de las protected_route y Jwt

```Python
JWT_SECRET_KEY="contraseña_privada_aleatoria"
```
## Conseguir el access_token
```Json
auth/login

{
 username:usuario_con_permisos
 password:password
}
```

## Uso del access_token
```Json
protected_route

headers:{
Authorization:access_token
},
body(OPCIONAL):{
 username:usuario_con_permisos
 password:password
}
