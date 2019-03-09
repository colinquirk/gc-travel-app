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
from gctravelparser.models import Question  # noqa: E402


with open('gctravelparser/static/questions.json') as f:
    questions = json.load(f)
    for q in questions:
        question = Question(
            is_active=True,
            in_basic_application=q['in_basic_application'],
            in_advanced_application=q['in_advanced_application'],
            slug=q['slug'],
            text=q['text'],
            word_limit=q['word_limit'],
            version_major=app.config['VERSION_NUMBER_MAJOR'],
            version_minor=app.config['VERSION_NUMBER_MINOR'],
            version_patch=app.config['VERSION_NUMBER_PATCH']
        )
        db.session.add(question)
    db.session.commit()
