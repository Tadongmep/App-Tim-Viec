from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from models import UserInformation, UserProfile, JobDescription, RecruiterInformation, Occupation
from models import db_session
import uuid
from auth import login_required
import json
import datetime

bp = Blueprint('recruiter', __name__, url_prefix='/v1/recruiter')

# def format_recruiter(recruiter):
#     return {

#     }


# get single recruiter
@bp.route('/getRecruiterInformation/<id>', methods=('GET', 'POST'))
@login_required
def get_recruiter_information(id):
    recruiter = db_session.query(RecruiterInformation).filter(
        RecruiterInformation.recruiter_uid == id).one()
    if recruiter is None:
        return 'No recruiter available.'
    else:
        temp = {}
        temp['recruiter_uid'] = str(recruiter.recruiter_uid)
        temp['user_id'] = str(recruiter.user_id)
        temp['business_code'] = recruiter.business_code
        temp['business_name_in_english'] = recruiter.business_name_in_english
        temp['business_name_in_abbreviations'] = recruiter.business_name_in_abbreviations
        temp['full_business_name'] = recruiter.full_business_name
        temp['address'] = recruiter.address
        temp['description'] = recruiter.description
        return {'recruiters': temp}

    return 'Wrong HTTP request methods!'


@bp.route('/createRecruiter', methods=('GET', 'POST'))
@login_required
def create_recruiter():
    if request.method == 'POST':
        if session['role'] != 'recruiter':
            return 'Permisson denied.'
        recruiter = db_session.query(RecruiterInformation).filter(
            RecruiterInformation.user_id == session['user_id']).first()
        if recruiter is not None:
            return 'Recruiter Information already created.'
        recruiter_id = uuid.uuid4()
        business_code = request.json['business_code']
        business_name_in_english = request.json['business_name_in_english']
        business_name_in_abbreviations = request.json['business_name_in_abbreviations']
        full_business_name = request.json['full_business_name']
        address = request.json['address']
        description = request.json['description']
        RI = RecruiterInformation()
        RI.recruiter_uid = recruiter_id
        RI.user_id = session['user_id']
        RI.business_code = business_code
        RI.business_name_in_english = business_name_in_english
        RI.business_name_in_abbreviations = business_name_in_abbreviations
        RI.full_business_name = full_business_name
        RI.address = address
        RI.description = description

        error = None

        if len(business_code) == 0:
            error = 'Business code is required.'
        if len(business_name_in_english) == 0:
            error = 'Business name in english is required.'
        if len(business_name_in_abbreviations) == 0:
            error = 'Business name in abbreviations is required.'
        if len(full_business_name) == 0:
            error = 'Full business name is required.'
        if len(address) == 0:
            error = 'Address is required.'

        if error is None:
            try:
                db_session.add(RI)
                db_session.commit()
            except:
                error = f"Failed to create recruiter information."
            else:
                return 'Create recruiter information successful.'
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


@bp.route('/editRecruiterInformation/<id>', methods=('GET', 'POST'))
@login_required
def edit_recruiter_information(id):
    if request.method == 'POST':
        if session['role'] != 'recruiter':
            return 'Permisson denied.'
        recruiter = db_session.query(RecruiterInformation).filter(
            RecruiterInformation.recruiter_uid == id).first()
        if recruiter is None:
            return 'Record is not exist.'
        business_code = request.json['business_code']
        business_name_in_english = request.json['business_name_in_english']
        business_name_in_abbreviations = request.json['business_name_in_abbreviations']
        full_business_name = request.json['full_business_name']
        address = request.json['address']
        description = request.json['description']
        recruiter.business_code = business_code
        recruiter.business_name_in_english = business_name_in_english
        recruiter.business_name_in_abbreviations = business_name_in_abbreviations
        recruiter.full_business_name = full_business_name
        recruiter.address = address
        recruiter.description = description
        recruiter.updated_at = datetime.datetime.utcnow()

        error = None

        if len(business_code) == 0:
            error = 'Business code is required.'
        if len(business_name_in_english) == 0:
            error = 'Business name in english is required.'
        if len(business_name_in_abbreviations) == 0:
            error = 'Business name in abbreviations is required.'
        if len(full_business_name) == 0:
            error = 'Full business name is required.'
        if len(address) == 0:
            error = 'Address is required.'

        if error is None:
            try:
                db_session.commit()
            except:
                error = f"Failed to change recruiter information."
            else:
                return 'Edit recruiter information successful.'
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


@bp.route('/createJobDescription', methods=('GET', 'POST'))
@login_required
def create_job_description():
    if request.method == 'POST':
        if session['role'] != 'recruiter':
            return 'Permisson denied.'
        recruiter = db_session.query(RecruiterInformation).filter(
            RecruiterInformation.user_id == session['user_id']).first()
        if recruiter is None:
            return 'Recruiter information is not exist.'
        # job_description = db_session.query(JobDescription).filter(
        #     JobDescription.recruiter_id == session['user_id']).first()
        # if recruiter is not None:
        #     return redirect(url_for("recruiter.edit_recruiter_information"))
        recruiter_id = str(recruiter.recruiter_uid)
        description = request.json['description']
        description_for_job = request.json['description_for_job']
        JD = JobDescription()
        JD.recruiter_id = recruiter_id
        JD.description = description
        for job in description_for_job:
            check_occupation = db_session.query(Occupation).filter(
                Occupation.job == job).first()
            if check_occupation is None:
                return f'New Job, Create occupation for {job} first.'
            JD.for_job.append(check_occupation)

        error = None

        if len(description) == 0:
            error = 'Description is required.'
        if len(description_for_job) == 0:
            error = 'Job is required.'

        if error is None:
            try:
                db_session.add(JD)
                db_session.commit()
            except:
                error = f"Failed to create job_description."
            else:
                return 'Create job_description successful.'
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


@bp.route('/editJobDescription/<id>', methods=('GET', 'POST'))
@login_required
def edit_job_description(id):
    if request.method == 'POST':
        if session['role'] != 'recruiter':
            return 'Permisson denied.'
        job_description = db_session.query(JobDescription).filter(
            JobDescription.id == id).one()
        if job_description is None:
            return 'Record is not exist.'
        description = request.json['description']
        description_for_job = request.json['description_for_job']
        job_description.description = description
        job_description.for_job.clear()
        for job in description_for_job:
            check_occupation = db_session.query(Occupation).filter(
                Occupation.job == job).first()
            if check_occupation is None:
                return 'New Job, Create occupation first.'
            job_description.for_job.append(check_occupation)
        job_description.updated_at = datetime.datetime.utcnow()

        error = None

        if len(description) == 0:
            error = 'Description is required.'

        if error is None:
            try:
                db_session.commit()
            except:
                error = f"Failed to edit Job Description."
            else:
                return 'Edit Job Description successful.'
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'


# Occupation
# @bp.route('/updateOccupation/', methods=('GET', 'POST'))
# @login_required
def update_occupation(job):
    # job = 'lap trinh giao dien'
    users = db_session.query(UserProfile).filter(
        UserProfile.job.contains(str(job))).all()
    error = 'success!'
    for user in users:
        print(user.job)
        check_occupation = db_session.query(Occupation).filter(
            Occupation.job == job).first()
        user.job_seeking.append(check_occupation)
        try:
            db_session.commit()
        except:
            error = 'update for user failed. please inform admin about this!'

    return error


@bp.route('/getOccupation', methods=('GET', 'POST'))
@login_required
def get_occupation():
    occupation = db_session.query(Occupation).all()
    if occupation is None:
        return 'No occupation available in database.'
    else:
        all_occupation = []
        for o in occupation:
            temp = {}
            temp['id'] = str(o.id)
            temp['specialization'] = o.specialization
            temp['job'] = o.job
            all_occupation.append(temp)
        return {'job description': all_occupation}

    return 'Wrong HTTP request methods!'


@bp.route('/createOccupation', methods=('GET', 'POST'))
@login_required
def create_occupation():
    if request.method == 'POST':
        if session['role'] != 'recruiter':
            return 'Permisson denied.'
        specialization = request.json['specialization']
        job = request.json['job']
        occupation = db_session.query(Occupation).filter(
            Occupation.job == job).first()
        if occupation is not None:
            return 'Job already exist.'
        O = Occupation()
        O.specialization = specialization
        O.job = job

        error = None

        if len(specialization) == 0:
            error = 'Specialization is required.'
        if len(job) == 0:
            error = 'Job is required.'
        if error is None:
            try:
                db_session.add(O)
                db_session.commit()
                update_occupation(job)
            except:
                error = f"Failed to create job."
            else:
                return 'Create job successful.'
        return error
        flash(error)

    return 'Wrong HTTP request methods!'


@bp.route('/editOccupation/<id>', methods=('GET', 'POST'))
@login_required
def edit_occupation(id):
    if request.method == 'POST':
        if session['role'] != 'recruiter':
            return 'Permisson denied.'
        occupation = db_session.query(Occupation).filter(
            Occupation.id == id).one()
        if occupation is None:
            return 'Record is not exist.'
        specialization = request.json['specialization']
        job = request.json['job']
        occupation.specialization = specialization
        occupation.job = job
        occupation.updated_at = datetime.datetime.utcnow()

        error = None

        if len(specialization) == 0:
            error = 'Specialization is required.'
        if len(job) == 0:
            error = 'Job is required.'

        if error is None:
            try:
                db_session.commit()
                update_occupation(job)
            except:
                error = f"Failed to edit Occupation."
            else:
                return 'Edit Job Occupation successful.'
        return error
        # flash(error)

    return 'Wrong HTTP request methods!'
