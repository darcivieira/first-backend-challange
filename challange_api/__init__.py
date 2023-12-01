from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from challange_api.settings import settings
from challange_api.utils.celery import create_celery

tags_metadata = [
    {
        "name": "Authentication",
        "description": "You must be authenticated to use some functionalities.",
    },
    {
        "name": "Users",
        "description": "Only to register an user, you can do it without authentication.",
    },
    {
        "name": "Wallets",
        "description": "You can see your wallet and do a direct update of the value."
    },
    {
        "name": "Transactions",
        "description": "You must provide the registration number of the recipient of the transaction."
    },
]

description = ""


def create_app() -> FastAPI:

    app = FastAPI(
        root_path="",
        servers=[
            {"url": "http://localhost", "description": "Local environment"},
        ],
        title='Challange Backend API',
        version='0.1.0',
        summary='This API was developed as part of a protfolio.',
        description=description,
        openapi_tags=tags_metadata
        # description=description,
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
