from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uvicorn

app = FastAPI()

# Cấu hình CORS
origins = [
    "https://test-deploy-web-to-vercel.vercel.app",  # Frontend đã deploy trên Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Chỉ định các nguồn gốc được phép
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (POST, GET, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các headers
)


class User(BaseModel):
    username: str
    password: str


@app.get("/")
async def hello_backend():
    return {"message": "hello backend"}


@app.post("/register")
async def register(user: User):
    try:
        conn = sqlite3.connect("/tmp/users.db")  # Đường dẫn cơ sở dữ liệu trong /tmp
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, user.password),
        )
        conn.commit()
        conn.close()
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
async def login(user: User):
    conn = sqlite3.connect("/tmp/users.db")  # Đường dẫn cơ sở dữ liệu trong /tmp
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (user.username, user.password),
    )
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8040, reload=True)
