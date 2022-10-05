from flask import current_app as app
# from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, declarative_base, scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
Base = declarative_base()
engine = create_engine('postgresql://postgres:123456@localhost/JobFinding')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()


class UserInformation(Base):
    __tablename__ = 'userInformation'
    user_uid = db.Column(UUID(as_uuid=True), index=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fullname = db.Column(db.String)
    role = db.Column(db.String)
    age = db.Column(db.Integer)
    sex = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self):
    #     return "<UserInformation(user_uid='%i' ,fullname='%s', age='%i', sex='%s')>" % (
    #         self.user_uid, self.fullname, self.age, self.sex)


user_occupation = db.Table('user_occupation',
                           Base.metadata,
                           db.Column('user_profile_id', db.Integer,
                                     db.ForeignKey('userProfile.id')),
                           db.Column('occupation_id', db.Integer,
                                     db.ForeignKey('occupation.id'))
                           )

user_jd = db.Table('user_jd',
                   Base.metadata,
                   db.Column('user_profile_id', db.Integer,
                             db.ForeignKey('userProfile.id')),
                   db.Column('job_jobDescription_id', db.Integer,
                             db.ForeignKey('jobDescription.id'))
                   )


class UserProfile(Base):
    __tablename__ = 'userProfile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(
        'userInformation.user_uid'))
    userInformation = relationship(
        "UserInformation", backref=backref("userProfile", uselist=False))
    height = db.Column(db.String)
    weight = db.Column(db.String)
    experience = db.Column(db.String)
    name_of_highschool = db.Column(db.String)
    identity_card_number = db.Column(db.String)
    interests = db.Column(db.String)
    character = db.Column(db.String)
    native_place = db.Column(db.String)
    education_level = db.Column(db.String)
    job = db.Column(db.String)
    job_seeking = db.relationship(
        'Occupation', secondary=user_occupation, backref='jobSeek')
    applied_job = db.relationship(
        'JobDescription', secondary=user_jd, backref='candidate')
    special_condition = db.Column(db.String)
    salary = db.Column(db.String)
    region = db.Column(db.String)
    province = db.Column(db.String)
    current_work_information = db.Column(db.String)
    degree_images = db.relationship('DegreeImage', backref='owner')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    # degree photo = db.Column()

    # def __repr__(self):
    #     return "<UserProfile(id='%i' ,user_id='%i', height='%i', weight='%s', experience='%s', name_of_highschool='%s', identity_card_number='%s', interests='%s', character='%s', native_place='%s', education_level='%s', job='%s', special_condition='%s', salary='%s', region='%s', province='%s', current_work_information='%s')>" % (
    #         self.id,
    #         self.user_id,
    #         self.height,
    #         self.weight,
    #         self.experience,
    #         self.name_of_highschool,
    #         self.identity_card_number,
    #         self.interests,
    #         self.character,
    #         self.native_place,
    #         self.education_level,
    #         self.job,
    #         self.special_condition,
    #         self.salary,
    #         self.region,
    #         self.province,
    #         self.current_work_information)


class DegreeImage(Base):
    __tablename__ = 'degreeImage'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('userProfile.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class RecruiterInformation(Base):
    __tablename__ = 'recruiterInformation'
    recruiter_uid = db.Column(UUID(as_uuid=True), index=True, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(
        'userInformation.user_uid'))
    userInformation = relationship(
        "UserInformation", backref=backref("recruiterId", uselist=False))
    business_code = db.Column(db.String)
    business_name_in_english = db.Column(db.String)
    business_name_in_abbreviations = db.Column(db.String)
    full_business_name = db.Column(db.String)
    address = db.Column(db.String)
    description = db.Column(db.String)
    jobDescriptions = db.relationship(
        "JobDescription", backref='recruiterInformation')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "{recruiter_uid='%s' ,user_id='%s', business_code='%s', business_name_in_english='%s', business_name_in_abbreviations='%s', full_business_name='%s', address='%s', description='%s', created_at='%s', updated_at='%s'}" % (
            self.recruiter_uid,
            self.user_id,
            self.business_code,
            self.business_name_in_english,
            self.business_name_in_abbreviations,
            self.full_business_name,
            self.address,
            self.description,
            self.created_at,
            self.updated_at)


occupation_JD = db.Table('occupation_JD',
                         Base.metadata,
                         db.Column('occupation_id', db.Integer,
                                   db.ForeignKey('occupation.id')),
                         db.Column('job_description_id', db.Integer,
                                   db.ForeignKey('jobDescription.id'))
                         )


class Occupation(Base):
    __tablename__ = 'occupation'
    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String)
    job = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class JobDescription(Base):
    __tablename__ = 'jobDescription'
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'recruiterInformation.recruiter_uid'))
    description = db.Column(db.String)
    for_job = db.relationship(
        'Occupation', secondary=occupation_JD, backref='jobFollow')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<RecruiterInformation(id='%i' ,description='%s', recruiter_id='%s')>" % (
            self.id, self.description, self.recruiter_id)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
    admin = UserInformation(user_uid=uuid.uuid4(), username='admin', password=generate_password_hash(
        '123456'), fullname='admin', role='admin', age='1', sex='admin')
    db_session.add(admin)
    db_session.commit()
