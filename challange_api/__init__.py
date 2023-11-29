from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    root_path="",
    servers=[
        {"url": "http://localhost:8000", "description": "Local environment"},
    ],
    title='ChallengeApi',
    version='0.1.0',
    description='API de desafio'
)

origins = [
    "http://apolo.panteu.com.br",
    "http://apolodev.panteu.com.br",
    "https://apolo.panteu.com.br",
    "https://apolodev.panteu.com.br",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
