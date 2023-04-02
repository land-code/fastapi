from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "fullname": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "fullname": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciales de autenticación inválidas",
                            headers={"WWW-Authenticate": "Bearer"})


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    return {"access_token": user.password, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
