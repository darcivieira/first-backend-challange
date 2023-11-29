from challange_api import app
from challange_api.routes.users import router as users
from challange_api.routes.wallet import router as wallet
from challange_api.routes.token import router as token
from challange_api.routes.transaction import router as transaction
from challange_api.generics.models import Model, engine

app.include_router(token)
app.include_router(users)
app.include_router(wallet)
app.include_router(transaction)

Model.metadata.create_all(engine)

