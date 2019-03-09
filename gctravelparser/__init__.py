from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['VERSION_NUMBER_MAJOR'] = 0
app.config['VERSION_NUMBER_MINOR'] = 1
app.config['VERSION_NUMBER_PATCH'] = 0
db = SQLAlchemy(app)

import gctravelparser.views  # noqa: F401,E402
import gctravelparser.models  # noqa: F401,E402

db.create_all()
db.session.commit()

# temp add questions from json
import json  # noqa: E402
from gctravelparser.models import Prompt  # noqa: E402


with open('gctravelparser/static/prompts.json') as f:
    prompts = json.load(f)
    for p in prompts:
        prompt = Prompt(
            is_active=True,
            in_basic_application=p['in_basic_application'],
            in_advanced_application=p['in_advanced_application'],
            slug=p['slug'],
            text=p['text'],
            word_limit=p['word_limit'],
            version_major=app.config['VERSION_NUMBER_MAJOR'],
            version_minor=app.config['VERSION_NUMBER_MINOR'],
            version_patch=app.config['VERSION_NUMBER_PATCH']
        )
        db.session.add(prompt)
    db.session.commit()
