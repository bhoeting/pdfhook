from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_marshmallow import Marshmallow
ma = Marshmallow()

from flask_migrate import Migrate
migrate = Migrate()