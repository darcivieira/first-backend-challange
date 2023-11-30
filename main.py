from challange_api import create_app
from challange_api import tasks
from challange_api.generics.models import Model, engine

Model.metadata.create_all(engine)

app = create_app()
celery = app.celery_app
