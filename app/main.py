from quart import Quart
from quart_schema import QuartSchema

from app.config.settings import settings
from app.routers.admin import admin_router
from app.routers.guest import guest_router
from app.routers.student import student_router

app = Quart(__name__)
app.secret_key = settings.SECRET_KEY

QuartSchema(app)

app.register_blueprint(admin_router)
app.register_blueprint(guest_router)
app.register_blueprint(student_router)

if __name__ == '__main__':
  app.run()