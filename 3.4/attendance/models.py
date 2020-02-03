from datetime import datetime as dt
from attendance import db, login_manager
from flask_login import UserMixin





#creating database table models


#employee table
class Employee(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key= True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    department_id=db.Column(db.Integer,db.ForeignKey('department.id'))
    name = db.Column(db.String(50))

    #employee backref can be used in attendence table t extract employee detail
    attendance = db.relationship('Attendance', backref='employee', lazy='dynamic')
    work = db.relationship('Work', backref='employee', lazy='dynamic')


#role table
class Role(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(2000))

    #role backref can be used in employeee table t extract  details
    employees = db.relationship('Employee', backref='role', lazy='dynamic')



#user table
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key= True)
    user_type = db.Column(db.String(30))
    password = db.Column(db.String(1000))

    #user backref can be used in employeee table t extract  details
    employees = db.relationship('Employee', backref='user', lazy='dynamic')



#department table
class Department(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(2000))

    #department backref can be used in employeee table t extract  details
    employees = db.relationship('Employee', backref='department', lazy='dynamic')



#attendance table
class Attendance(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    employee_id = db.Column(db.Integer,db.ForeignKey('employee.id'))
    in_out=  db.Column(db.String(30))
    DT = db.Column(db.DateTime, default=dt.now())



#holiday table containing list of holidays
class Holidays(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    date = db.Column(db.Date)



#work table containing list of work hours and leaves
class Work(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    date = db.Column(db.Date)
    work_hours= db.Column(db.Time)
    leaves=db.Column(db.Integer)
    employee_id= db.Column(db.Integer,db.ForeignKey('employee.id'))

