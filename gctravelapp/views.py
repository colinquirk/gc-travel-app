from datetime import datetime
from uuid import uuid4
from flask import redirect, render_template, request, url_for
from gctravelapp import app, db
from gctravelapp.models import (
    Applicant, Application, Recommendation, Review, Reviewer, Prompt, Response, Question, Rating
)


def get_applicant(form):
    """ Gets applicant info, or adds if necessary
    """
    applicant_result = Applicant.query.filter_by(email=form.get("email")).first()

    if applicant_result:
        applicant_id = applicant_result.applicant_id
    else:
        applicant_id = add_applicant(form)

    return applicant_id


def add_applicant(form):
    """ Adds new applicant to database
    """
    applicant = Applicant(
        first_name=form.get("firstname"),
        last_name=form.get("lastname"),
        email=form.get("email"),
        division=form.get("division")
    )
    db.session.add(applicant)
    db.session.commit()

    return applicant.applicant_id


def get_reviewer(form):
    """ Gets reviewer info, or adds if necessary
    """
    reviewer = Reviewer.query.filter_by(email=form.get("reviewer-email")).first()

    if reviewer:
        reviewer_id = reviewer.reviewer_id
    else:
        reviewer_id = add_reviewer(form)

    return reviewer_id


def add_reviewer(form):
    """ Adds new reviewer to database
    """
    reviewer = Reviewer(
        first_name=form.get("reviewer-firstname"),
        last_name=form.get("reviewer-lastname"),
        email=form.get("reviewer-email"),
    )
    db.session.add(reviewer)
    db.session.commit()

    return reviewer.reviewer_id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    if request.form:
        application = Application(
            submitted=datetime.now(),
            application_type='basic',
            status='submitted',
            applicant_id=get_applicant(request.form),
            event_name=request.form.get('event-name'),
            travel_start=datetime.strptime(request.form.get('start-date'), '%Y-%m-%d'),
            travel_end=datetime.strptime(request.form.get('end-date'), '%Y-%m-%d'),
            faculty_name=request.form.get('faculty-name'),
            faculty_email=request.form.get('faculty-email'),
            group_size=request.form.get('group-size'),
            uuid=str(uuid4())
        )
        db.session.add(application)

        for slug, response_text in request.form.items():
            prompt = (
                Prompt.query.filter_by(slug=slug)
                .filter_by(is_active=True)
                .filter_by(in_basic_application=True)
                .first()
            )
            if prompt:
                response = Response(
                    application_id=application.application_id,
                    prompt_id=prompt.prompt_id,
                    text=response_text
                )
                db.session.add(response)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('basic.html', prompts=Prompt.query.filter_by(in_basic_application=True))


@app.route('/advanced', methods=['GET', 'POST'])
def advanced():
    if request.form:
        application = Application(
            submitted=datetime.now(),
            application_type='advanced',
            status='submitted',
            applicant_id=get_applicant(request.form),
            event_name=request.form.get('event-name'),
            travel_start=datetime.strptime(request.form.get('start-date'), '%Y-%m-%d'),
            travel_end=datetime.strptime(request.form.get('end-date'), '%Y-%m-%d'),
            faculty_name=request.form.get('faculty-name'),
            faculty_email=request.form.get('faculty-email'),
            presentation_type=request.form.get('presentation-type'),
            uuid=str(uuid4())
        )
        db.session.add(application)

        for slug, response_text in request.form.items():
            prompt = (
                Prompt.query.filter_by(slug=slug)
                .filter_by(is_active=True)
                .filter_by(in_advanced_application=True)
                .first()
            )
            if prompt:
                response = Response(
                    application_id=application.application_id,
                    prompt_id=prompt.prompt_id,
                    text=response_text
                )
                db.session.add(response)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('advanced.html', prompts=Prompt.query.filter_by(in_advanced_application=True))


@app.route('/recommendation/<uuid:uuid>', methods=['GET', 'POST'])
def recommendation(uuid):
    if request.form:
        recommendation = Recommendation(
            application_id=Application.query.filter_by(uuid=str(uuid)).first().application_id,
            student_first_name=request.form.get('student-firstname'),
            student_last_name=request.form.get('student-lastname'),
            recommender_first_name=request.form.get('recommender-firstname'),
            recommender_last_name=request.form.get('recommender-lastname'),
            recommender_email=request.form.get('recommender-email'),
            recommender_position=request.form.get('recommender-position'),
            relationship=request.form.get('relationship'),
            merit=request.form.get('merit'),
            conference=request.form.get('conference'),
            representative=request.form.get('representative'),
            additional_comments=request.form.get('additional-comments')
        )

        db.session.add(recommendation)

        application_result = Application.query.filter_by(uuid=str(uuid)).first()
        application_result.status = 'reviewing'

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('recommendation.html')


@app.route('/review/basic/<uuid:uuid>/<int:review_number>', methods=['GET', 'POST'])
def basic_review(uuid, review_number):
    application = (
        Application.query
        .filter_by(uuid=str(uuid))
        .join(Applicant)
        .first()
    )

    if request.form:
        review = Review(
            reviewer_id=get_reviewer(request.form),
            application_id=application.application_id,
            review_number=review_number,
            overall_strength=request.form.get("overall-strength"),
            additional_comments=request.form.get("additional-comments")
        )
        db.session.add(review)
        db.session.commit()

        for slug, score in request.form.items():
            question = (
                Question.query
                .filter_by(slug=slug)
                .join(Prompt)
                .filter_by(is_active=True)
                .filter_by(in_basic_application=True)
                .first()
            )
            if question:
                rating = Rating(
                    review_id=review.review_id,
                    question_id=question.question_id,
                    value=score
                )
                db.session.add(rating)

        db.session.commit()

        return redirect(url_for('index'))

    questions = (
        Question.query
        .join(Prompt)
        .filter_by(is_active=True)
        .filter_by(in_basic_application=True)
        .all()
    )

    prompts = (
        Prompt.query
        .filter_by(is_active=True)
        .filter_by(in_basic_application=True)
        .all()
    )

    responses = (
        Response.query
        .join(Prompt)
        .filter_by(is_active=True)
        .filter_by(in_basic_application=True)
        .all()
    )

    return render_template(
        'review_basic.html',
        first_name=application.applicant.first_name,
        last_name=application.applicant.last_name,
        email=application.applicant.email,
        division=application.applicant.division,
        group_size=application.group_size,
        travel_start=application.travel_start,
        travel_end=application.travel_end,
        event_name=application.event_name,
        faculty_name=application.faculty_name,
        faculty_email=application.faculty_email,
        prompts=prompts,
        questions=questions,
        responses=responses
    )


@app.route('/review/advanced/<uuid:uuid>/<int:review_number>', methods=['GET', 'POST'])
def advanced_review(uuid, review_number):
    application = (
        Application.query
        .filter_by(uuid=str(uuid))
        .join(Applicant)
        .first()
    )

    if request.form:
        review = Review(
            reviewer_id=get_reviewer(request.form),
            application_id=application.application_id,
            review_number=review_number,
            overall_strength=request.form.get("overall-strength"),
            additional_comments=request.form.get("additional-comments")
        )
        db.session.add(review)
        db.session.commit()

        for slug, score in request.form.items():
            question = (
                Question.query
                .filter_by(slug=slug)
                .join(Prompt)
                .filter_by(is_active=True)
                .filter_by(in_advanced_application=True)
                .first()
            )
            if question:
                rating = Rating(
                    review_id=review.review_id,
                    question_id=question.question_id,
                    value=score
                )
                db.session.add(rating)

        db.session.commit()

        return redirect(url_for('index'))

    questions = (
        Question.query
        .join(Prompt)
        .filter_by(is_active=True)
        .filter_by(in_advanced_application=True)
        .all()
    )

    prompts = (
        Prompt.query
        .filter_by(is_active=True)
        .filter_by(in_advanced_application=True)
        .all()
    )

    responses = (
        Response.query
        .join(Prompt)
        .filter_by(is_active=True)
        .filter_by(in_advanced_application=True)
        .all()
    )

    return render_template(
        'review_basic.html',
        first_name=application.applicant.first_name,
        last_name=application.applicant.last_name,
        email=application.applicant.email,
        division=application.applicant.division,
        group_size=application.group_size,
        travel_start=application.travel_start,
        travel_end=application.travel_end,
        event_name=application.event_name,
        faculty_name=application.faculty_name,
        faculty_email=application.faculty_email,
        prompts=prompts,
        questions=questions,
        responses=responses
    )


@app.route('/review')
def review_landing():
    return render_template('review_landing.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
