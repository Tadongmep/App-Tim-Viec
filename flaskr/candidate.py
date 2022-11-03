from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, send_from_directory
)
from models import UserInformation, UserProfile, JobDescription, Occupation, user_occupation, occupation_JD, RecruiterInformation, DegreeImage
from models import db_session
import uuid
from auth import login_required
import datetime
from sqlalchemy import or_
# from app import ALLOWED_EXTENSIONS
import os
from werkzeug.utils import secure_filename
import random
import string

bp = Blueprint('candidate', __name__, url_prefix='/v1/candidate')


@bp.route('/createProfile', methods=('GET', 'POST'))
@login_required
def create_profile():
    if request.method == 'POST':
        user = db_session.query(UserProfile).filter(
            UserProfile.user_id == session['user_id']).first()
        if user is not None:
            return redirect(url_for("candidate.get_profile"))
        else:
            user_id = session['user_id']
            height = request.json['height']
            weight = request.json['weight']
            experience = request.json['experience']
            name_of_highschool = request.json['name_of_highschool']
            identity_card_number = request.json['identity_card_number']
            interests = request.json['interests']
            character = request.json['character']
            native_place = request.json['native_place']
            education_level = request.json['education_level']
            job = request.json['job']
            special_condition = request.json['special_condition']
            salary = request.json['salary']
            region = request.json['region']
            province = request.json['province']
            current_work_information = request.json['current_work_information']

            error = None

            job_string = ", ".join(job)

            if len(height) == 0:
                error = 'Height is required.'
            if len(weight) == 0:
                error = 'Weight is required.'
            if len(education_level) == 0:
                error = 'Education level is required.'
            # if len(job) == 0:
            #     error = 'Job is required.'
            if len(identity_card_number) == 0:
                error = 'Identity card number is required.'
            if len(native_place) == 0:
                error = 'Native place is required.'
            if len(region) == 0:
                error = 'Region card number is required.'
            if len(province) == 0:
                error = 'Province place is required.'

            if error is None:
                UP = UserProfile()
                UP.user_id = user_id
                UP.height = height
                UP.weight = weight
                UP.experience = experience
                UP.name_of_highschool = name_of_highschool
                UP.identity_card_number = identity_card_number
                UP.interests = interests
                UP.character = character
                UP.native_place = native_place
                UP.education_level = education_level
                UP.job = job_string
                UP.special_condition = special_condition
                UP.salary = salary
                UP.region = region
                UP.province = province
                UP.current_work_information = current_work_information
                # try:
                warn_msg = None
                job_not_support = []
                for j in job:
                    check_occupation = db_session.query(Occupation).filter(
                        Occupation.job == j).first()
                    if check_occupation is None:
                        job_not_support.append(j)
                        # warn_msg = f"The {j} doesn't exist in database yet so there are no recruiter looking for {j} right now."
                    else:
                        UP.job_seeking.append(check_occupation)
                str_formated = ", ".join(job_not_support)
                warn_msg = f"The {str_formated} doesn't exist in database yet so there are no recruiter looking for {str_formated} right now."
                db_session.add(UP)
                db_session.commit()
                return {
                    'message': 'Create profile successful.',
                    'warning': warn_msg
                }

                # except:
                #     return 'Failed to create profile.'
        return error

    return 'Wrong HTTP request methods!'


@bp.route('/editProfile/<id>', methods=('GET', 'POST'))
@login_required
def edit_profile(id):
    if request.method == 'POST':
        user = db_session.query(UserProfile).filter(
            UserProfile.id == id).first()

        user.height = request.json['height']
        user.weight = request.json['weight']
        user.experience = request.json['experience']
        user.name_of_highschool = request.json['name_of_highschool']
        user.identity_card_number = request.json['identity_card_number']
        user.interests = request.json['interests']
        user.character = request.json['character']
        user.native_place = request.json['native_place']
        user.education_level = request.json['education_level']
        job_list = request.json['job']
        user.job = ", ".join(job_list)
        user.special_condition = request.json['special_condition']
        user.salary = request.json['salary']
        user.region = request.json['region']
        user.province = request.json['province']
        user.current_work_information = request.json['current_work_information']
        user.updated_at = datetime.datetime.utcnow()

        error = None

        if len(user.height) == 0:
            error = 'Height is required.'
        if len(user.weight) == 0:
            error = 'Weight is required.'
        if len(user.education_level) == 0:
            error = 'Education level is required.'
        # if len(user.job) == 0:
        #     error = 'Job is required.'
        if len(user.identity_card_number) == 0:
            error = 'Identity card number is required.'
        if len(user.native_place) == 0:
            error = 'Native place is required.'
        if len(user.region) == 0:
            error = 'Region card number is required.'
        if len(user.province) == 0:
            error = 'Province place is required.'

        user.job_seeking.clear()
        warn_msg = None
        job_not_support = []
        for j in job_list:
            check_occupation = db_session.query(Occupation).filter(
                Occupation.job == j).first()
            if check_occupation is None:
                job_not_support.append(j)
            else:
                user.job_seeking.append(check_occupation)
        str_formated = ", ".join(job_not_support)
        warn_msg = f"The {str_formated} doesn't exist in database yet so there are no recruiter looking for {str_formated} right now."

        if error is None:
            try:
                db_session.commit()
                return {
                    'message': 'Edt profile successful.',
                    'warning': warn_msg
                }
            except:
                return 'Failed to edit profile.'
        return error

    return 'Wrong HTTP request methods!'


@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def get_profile():
    user = db_session.query(UserProfile).filter(
        UserProfile.user_id == session['user_id']).first()
    if user is None:
        return redirect(url_for("candidate.create_profile"))
    else:
        return {
            "message": "success",
            "data": {
                "_id": user.user_id,
                "height": user.height,
                "weight": user.weight,
                "experience": user.experience,
                "name_of_highschool": user.name_of_highschool,
                "identity_card_number": user.identity_card_number,
                "interests": user.interests,
                "character": user.character,
                "native_place": user.native_place,
                "education_level": user.education_level,
                "job": user.job,
                "special_condition": user.special_condition,
                "salary": user.salary,
                "region": user.region,
                "province": user.province,
                "current_work_information": user.current_work_information

            }
        }

    return 'Wrong HTTP request methods!'


# Occupation
@bp.route('/getJobDescriptionByJob', methods=('GET', 'POST'))
@login_required
def get_job_description_by_job():
    user = db_session.query(UserProfile).filter(
        UserProfile.user_id == session['user_id']).first()
    if user is None:
        return 'No profile found! please create it.'
    all_job_description = []
    for js in user.job_seeking:
        for single_jd in js.jobFollow:
            temp = {}
            temp['id'] = str(single_jd.id)
            temp['recruiter_id'] = str(single_jd.recruiter_id)
            temp['description'] = single_jd.description
            temp['created_at'] = single_jd.created_at
            temp['updated_at'] = single_jd.updated_at
            all_job_description.append(temp)
    return {'job description': all_job_description}


@bp.route('/getJobDescriptionByRegion', methods=('GET', 'POST'))
@login_required
def get_job_description_by_region():
    user = db_session.query(UserProfile).filter(
        UserProfile.user_id == session['user_id']).first()
    if user is None:
        return 'No profile found! please create it.'

    recruiters = db_session.query(RecruiterInformation).filter(or_(RecruiterInformation.address.contains(
        user.region), RecruiterInformation.address.contains(user.province))).all()

    all_job_description = []
    for recruiter in recruiters:
        for jd in recruiter.jobDescriptions:
            temp = {}
            temp['id'] = str(jd.id)
            temp['recruiter_id'] = str(jd.recruiter_id)
            temp['description'] = jd.description
            temp['created_at'] = jd.created_at
            temp['updated_at'] = jd.updated_at
            all_job_description.append(temp)
    return {'job description': all_job_description}


@bp.route('/applyForJob', methods=('GET', 'POST'))
@login_required
def apply_for_job():
    job_description_id = request.json['job description id']
    # error = None
    user = db_session.query(UserProfile).filter(
        UserProfile.user_id == session['user_id']).first()
    if user is None:
        return 'No profile found! please create it.'
    if job_description_id is None:
        flash('No job description id supply!')
    jd = db_session.query(JobDescription).filter(
        JobDescription.id == str(job_description_id)).first()
    if jd is None:
        flash('No job description found!')
    try:
        user.applied_job.append(jd)
        db_session.commit()
    except:
        return 'Error. Apply failed!'
    return {'message': 'apply successful.'}

# Degree Image


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@bp.route('/uploadDegreeImage', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        try:
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
        except OSError:
            pass
        if 'files' not in request.files:
            return 'No file part'
        files = request.files.getlist('files')
        user = db_session.query(UserProfile).filter(
            UserProfile.user_id == session['user_id']).first()
        if user is None:
            return 'No user_id found.'
        for file in files:
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(
                    get_random_string(10) + file.filename)
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename))

                image = DegreeImage()
                image.file_name = filename
                image.owner_id = user.id
                try:
                    db_session.add(image)
                    db_session.commit()
                except:
                    return 'Upload failed.'
            # print(file)
            # return 'Upload successful.'
    return 'Upload successful.'
    # '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=files multiple>
    #   <input type=submit value=Upload>
    # </form>
    # '''


@bp.route('/deleteDegreeImage/<id>', methods=['GET', 'POST'])
@login_required
def delete_file(id):
    image = db_session.query(DegreeImage).filter(
        DegreeImage.id == id).first()
    try:
        db_session.delete(image)
        db_session.commit()
    except:
        return 'Delete failed.'
    return 'Delete successful.'


@bp.route('/displayDegreeImage')
@login_required
def display_image():
    user = db_session.query(UserProfile).filter(
        UserProfile.user_id == session['user_id']).first()
    # print(user.user_id)
    url_images = []
    for img in user.degree_images:
        temp = {}
        temp['url'] = url_for('static', filename='images/' + img.file_name)
        url_images.append(temp)
    
    # print(url_images)
    return url_images
