from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from challange_api.settings import settings
from challange_api.utils.celery import create_celery


def create_app() -> FastAPI:

    app = FastAPI(
        root_path="",
        servers=[
            {"url": "http://localhost", "description": "Local environment"},
        ],
        title='ChallengeApi',
        version='0.1.0',
        description='API de desafio'
    )

    app.celery_app = create_celery()

    origins = [
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

    from challange_api.routes.users import router as users
    from challange_api.routes.wallet import router as wallet
    from challange_api.routes.token import router as token
    from challange_api.routes.transaction import router as transaction
    from challange_api.generics.models import Model, engine

    app.include_router(token)
    app.include_router(users)
    app.include_router(wallet)
    app.include_router(transaction)

    return app
