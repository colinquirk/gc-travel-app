from gctravelparser import db


class Applicant(db.Model):
    """ A class containing information about the user who submitted the application
    """
    applicant_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    division = db.Column(db.String(60), nullable=False)
    last_awarded = db.Column(db.DateTime, nullable=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)


class Reviewer(db.Model):
    """ A class containing information about the user who reviewed the application
    """
    reviewer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_reviewed = db.Column(db.DateTime, nullable=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)


class Application(db.Model):
    """ A class containing information about the application itself
    """
    application_id = db.Column(db.Integer, primary_key=True)
    application_type = db.Column(db.String(50), nullable=False)
    submitted = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.applicant_id'), nullable=False)
    event_name = db.Column(db.String(255), nullable=False)
    travel_start = db.Column(db.DateTime, nullable=False)
    travel_end = db.Column(db.DateTime, nullable=False)
    faculty_name = db.Column(db.String(80), nullable=False)
    faculty_email = db.Column(db.String(120), nullable=False)
    group_size = db.Column(db.Integer, nullable=True)
    presentation_type = db.Column(db.String(50), nullable=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='application', lazy=True)
    responses = db.relationship('Response', backref='application', lazy=True)


class Recommendation(db.Model):
    """ A class containing information about a recommendation
    """
    recommendation_id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'), nullable=False)
    student_first_name = db.Column(db.String(60), nullable=False)
    student_last_name = db.Column(db.String(60), nullable=False)
    recommender_first_name = db.Column(db.String(60), nullable=False)
    recommender_last_name = db.Column(db.String(60), nullable=False)
    recommender_email = db.Column(db.String(120), nullable=False)
    recommender_position = db.Column(db.String(60), nullable=False)
    relationship = db.Column(db.String(60), nullable=False)
    merit = db.Column(db.Text, nullable=True)  # TODO Factor this out too
    conference = db.Column(db.Text, nullable=True)
    representative = db.Column(db.Text, nullable=True)
    additional_comments = db.Column(db.Text, nullable=True)


class Review(db.Model):
    """ A class containing information about a review
    """
    review_id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.reviewer_id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'), nullable=False)
    review_number = db.Column(db.Integer, nullable=False)
    ratings = db.relationship('Rating', backref='review', lazy=True)


class Prompt(db.Model):
    """ A class containing information about the prompts to be asked
    """
    prompt_id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, nullable=False)
    in_basic_application = db.Column(db.Boolean, nullable=False)
    in_advanced_application = db.Column(db.Boolean, nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    word_limit = db.Column(db.Integer, nullable=True)
    version_major = db.Column(db.Integer, nullable=False)
    version_minor = db.Column(db.Integer, nullable=False)
    version_patch = db.Column(db.Integer, nullable=False)
    responses = db.relationship('Response', backref='prompt', lazy=True)


class Response(db.Model):
    """ A class containing information about the application responses
    """
    response_id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.prompt_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)


class Question(db.Model):
    """ A class containing information about the questions on reviews
    """
    question_id = db.Column(db.Integer, primary_key=True)


class Rating(db.Model):
    """ A class containing ratings from reviews
    """
    rating_id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.review_id'), nullable=False)
