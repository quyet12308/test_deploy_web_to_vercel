from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import sqlite3
import uvicorn

from fastapi.middleware.cors import (
    CORSMiddleware,
)

app = FastAPI()

# Cấu hình CORS
origins = [
    "http://localhost",  # Nguồn gốc của bạn frontend local
    "http://localhost:8040",  # Nguồn gốc của bạn backend local
    "https://your-frontend-url.vercel.app",  # URL của frontend đã deploy trên Vercel
    "http://127.0.0.1:5500",
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
    return "hello backend"


@app.post("/register")
async def register(user: User, request: Request):
    try:
        data = await request.json()
        print(f"Received register data: {data}")  # Log dữ liệu nhận được để kiểm tra
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, user.password),
    )
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(user: User, request: Request):
    try:
        data = await request.json()
        print(f"Received login data: {data}")  # Log dữ liệu nhận được để kiểm tra
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    conn = sqlite3.connect("users.db")
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
