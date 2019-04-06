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
    application = db.relationship('Application', backref='applicant', lazy=True)
    reviews = db.relationship('Review', backref='applicant', lazy=True)


class Reviewer(db.Model):
    """ A class containing information about the user who reviewed the application
    """
    reviewer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_reviewed = db.Column(db.DateTime, nullable=True)
    review = db.relationship('Review', backref='reviewer', lazy=True)


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
    importance = db.Column(db.Text, nullable=False)  # How often do questions change?
    significance = db.Column(db.Text, nullable=True)
    contribution = db.Column(db.Text, nullable=False)
    expenditures = db.Column(db.Text, nullable=False)
    alternative_funding = db.Column(db.Text, nullable=True)
    faculty_name = db.Column(db.String(80), nullable=False)
    faculty_email = db.Column(db.String(120), nullable=False)
    group_size = db.Column(db.Integer, nullable=True)
    presentation_type = db.Column(db.String(50), nullable=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)


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
    merit = db.Column(db.Text, nullable=True)
    conference = db.Column(db.Text, nullable=True)
    representative = db.Column(db.Text, nullable=True)
    additional_comments = db.Column(db.Text, nullable=True)


class Review(db.Model):
    """ A class containing information about a review
    """
    review_id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.reviewer_id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.applicant_id'), nullable=False)
    review_number = db.Column(db.Integer, nullable=False)
    event_relevance = db.Column(db.Integer, nullable=False)
    participation_justification = db.Column(db.Integer, nullable=False)
    competitiveness = db.Column(db.Integer, nullable=True)
    academic_value = db.Column(db.Integer, nullable=True)
    graduate_experience = db.Column(db.Integer, nullable=True)
    importance_clear_organization = db.Column(db.Integer, nullable=False)
    importance_comments = db.Column(db.Text, nullable=True)
    purpose_clear = db.Column(db.Integer, nullable=True)
    significance_explained = db.Column(db.Integer, nullable=True)
    larger_context = db.Column(db.Integer, nullable=True)
    clear_presentation = db.Column(db.Integer, nullable=True)
    significance_comments = db.Column(db.Text, nullable=True)
    clear_commitment = db.Column(db.Integer, nullable=False)
    help_peers_plan = db.Column(db.Integer, nullable=False)
    contribution_clear_organization = db.Column(db.Integer, nullable=False)
    contribution_comments = db.Column(db.Text, nullable=True)
    merit_funding = db.Column(db.Integer, nullable=False)
    overall_comments = db.Column(db.Text, nullable=True)
