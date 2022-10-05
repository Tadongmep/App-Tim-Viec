from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from models import UserInformation, UserProfile, JobDescription, RecruiterInformation, Occupation
from models import db_session
import uuid
from auth import login_required
import json
import datetime

bp = Blueprint('sharedOperation', __name__, url_prefix='/v1')

# get all jd
@bp.route('/getJobsDescription', methods=('GET', 'POST'))
@login_required
def get_jobs_description():
    job_description = db_session.query(JobDescription).order_by(
        JobDescription.created_at.desc()).all()
    if job_description is None:
        return 'No job description available.'
    else:
        all_job_description = []
        for jd in job_description:
            temp = {}
            temp['id'] = str(jd.id)
            temp['recruiter_id'] = str(jd.recruiter_id)
            temp['description'] = jd.description
            all_job_description.append(temp)
        return {'job description': all_job_description}

    return 'Wrong HTTP request methods!'


# get single jd
@bp.route('/getJobDescription/<id>', methods=('GET', 'POST'))
@login_required
def get_job_description(id):
    job_description = db_session.query(JobDescription).filter(
        JobDescription.id == id).one()
    if job_description is None:
        return 'No job description available.'
    else:
        temp = {}
        temp['id'] = str(job_description.id)
        temp['recruiter_id'] = str(job_description.recruiter_id)
        temp['description'] = job_description.description
        return {'job description': temp}

    return 'Wrong HTTP request methods!'

# get all recruiter
@bp.route('/getRecruitersInformation', methods=('GET', 'POST'))
@login_required
def get_recruiters_information():
    recruiter = db_session.query(RecruiterInformation).all()
    if recruiter is None:
        return 'No recruiter available.'
    else:
        all_recruiter = []
        for recruiter in recruiter:
            temp = {}
            temp['recruiter_uid'] = str(recruiter.recruiter_uid)
            temp['user_id'] = str(recruiter.user_id)
            temp['business_code'] = recruiter.business_code
            temp['business_name_in_english'] = recruiter.business_name_in_english
            temp['business_name_in_abbreviations'] = recruiter.business_name_in_abbreviations
            temp['full_business_name'] = recruiter.full_business_name
            temp['address'] = recruiter.address
            temp['description'] = recruiter.description
            all_recruiter.append(temp)
        return {'recruiters': all_recruiter}

    return 'Wrong HTTP request methods!'