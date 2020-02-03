"""Web App for storing working hours, leaves,attendence
CHANGEABLE datetime(TOMMOROW)"""

from flask import Flask, render_template, request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
from flask_login import LoginManager 
from flask_login import login_user, logout_user, login_required, current_user, UserMixin




#initializing flask app
app = Flask(__name__)

#location of database
URI= 'mysql+pymysql://root:@localhost:3306/aps2'

#configuring the uri
app.config['SQLALCHEMY_DATABASE_URI'] = URI

#initializing the database object
db= SQLAlchemy(app)

#used for protection from modifying cookies
app.secret_key = "shhhh...iAmASecret!"


#initializing login manager
login_manager = LoginManager(app)

#redirects to login function if user is not loged in
login_manager.login_view = 'login'


#create association with actual user data in the database
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))




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
    DT = db.Column(db.DateTime)



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







#Routes



#submit page
@app.route("/")
def submit():

    return render_template('submit.html')



#sucess page
@app.route("/success", methods=['POST'])
def success():

    #extracting submit detail
    employee_id= request.form["employee_id"]
        
     
    emp= Employee.query.all()
    







    #USER DEFINED DATETIME(tomorow)
    #USER DEFINED DATETIME(tomorow)
    #USER DEFINED DATETIME(tomorow)
    dd1=dt.now()
    tomorow = dd1 - timedelta(days = 6,hours= 2) 
    #USER DEFINED DATETIME(tomorow)
    #USER DEFINED DATETIME(tomorow)
    #USER DEFINED DATETIME(tomorow)







    #checking if the current day is saturday or sunday or not, strftime('%A') returns day in string format
    if tomorow.strftime('%A')!="Saturday" and tomorow.strftime('%A')!= "Sunday":
        for i in emp:

            #checking if curent date is in holidays table, adding leaves for all employess for current date if condition is satisfied
            if Work.query.filter_by(date=tomorow.date(), employee_id= i.id).count() != 1 and Holidays.query.filter_by(date=tomorow.date()).count() !=1 :
                data= Work(date= tomorow,leaves= 1, employee_id=i.id)
                db.session.add(data)
                db.session.commit()


    

    #checking if id is present in employee table
    if Employee.query.filter_by(id= employee_id).count() != 0 :
        

        #determining if the reponse is for sign in or out
        x= Attendance.query.filter_by(employee_id= employee_id).count()
        if x%2==0:
            inout="in"
        else :
            inout="out"
        
        
        #adding data to attendance table
        data= Attendance(employee_id=employee_id,in_out=inout,DT= tomorow)
        db.session.add(data)
        db.session.commit()

    
        
        data1=Attendance.query.filter_by(employee_id=employee_id, in_out= "in")[-1]
        
    
        #converting the datetime format to string time forma
        hour1=data1.DT.strftime("%H:%M:%S")


        #converting the datetime format to date format
        day = data.DT.date()
        
        if data.in_out == "in":           

            return render_template("submit.html", text= "sigin in")



        elif data.in_out=="out":
            hour2 = data.DT.strftime("%H:%M:%S")
            
            #time difference between sign in and out,converting the string time format to time format
            t1 = dt.strptime( hour2, "%H:%M:%S")-dt.strptime( hour1, "%H:%M:%S")


            #add data if row doesn't exist
            if Work.query.filter_by(date=day,employee_id=employee_id).count()==0:
                db.session.add(Work(date=day,work_hours=t1,leaves=0,employee_id=employee_id))
                db.session.commit()
            
            
            #replace data if row exist for work_hours value = None
            elif Work.query.filter_by(date=day,employee_id=employee_id, work_hours= None).count()==1:
                dataa= Work.query.filter_by(date=day,employee_id=employee_id, work_hours= None).first()
                dataa.date= day
                dataa.work_hours= t1
                dataa.leaves=0
                dataa.employee_id= employee_id
                db.session.commit()

            
            #update work_hours if row already exist
            elif Work.query.filter_by(date=day,employee_id=employee_id).count() ==1:
                data2=Work.query.filter_by(date=day,employee_id=employee_id).first()


                if data2.work_hours != None:
                    t2=data2.work_hours.strftime("%H:%M:%S.%f")
                    time_total=t1+ dt.strptime(t2, "%H:%M:%S.%f")
                    data2.work_hours=time_total
                    db.session.commit()

            return render_template("submit.html", text="sign out")
        else:
            pass

        
    else:
        return render_template("submit.html", text="Seems like we got wrong employee id")





#login page get
@app.route("/login")
def login():

    return render_template("login.html")



#login page post
@app.route("/login", methods=['POST'])
def login_post():
    

    #extracting the data submited
    login_id = request.form["id"]
    password = request.form["password"]


    #filtering emploee row from employee table
 

    employe1=Employee.query.filter_by(id= login_id).first()

    #checking the login details from user and employee table
    
    if employe1.user.user_type== "admin"  and employe1.user.password == password:
 
        login_user(employe1)

        return redirect(url_for('admin'))

    return render_template("login.html",text='Please check your login details and try again.')




#admin page
@app.route("/admin")

#login_required let the fuction execute only if user is loged in
@login_required
def admin():
    

    #creating a dataframe from employee table
    data = pd.read_sql_table("employee",URI)


    #creating new columns
    for n in range(len(data.id)):
        data["Departmet"]="none"
        data["Role"]="none"
        data["User"]="none"

    
    #adding values to column
    for n in range(len(data.id)):
        data["Departmet"][n]=Employee.query.filter_by(id= int(data.id[n])).first().department.name
        data["Role"][n]=Employee.query.filter_by(id= int(data.id[n])).first().role.name
        data["User"][n]=Employee.query.filter_by(id= int(data.id[n])).first().user.user_type



    #deleting unwanted column from dataframe
    data.drop(["role_id","user_id","department_id"], axis = 1, inplace = True)

    return render_template('admin.html',text= data.to_html())







#work_hours get page
@app.route("/WORK")

#login_required let the fuction execute only if user is loged in
@login_required

def work():


    #creating a dataframe(DF) from work table
    DF = pd.read_sql_table("work",URI)


    #creating new columns
    for n in range(len(DF.id)):
        DF["Employee Name"]="none"


    
    #adding values to column
    for n in range(len(DF.id)):
        DF["Employee Name"][n]=Work.query.filter_by(id= int(DF.id[n])).first().employee.name




    #creating new columns,and adding year_month to it
    DF["year_month"]=pd.to_datetime(DF.date).dt.to_period('M')

    #extracting the data with year_month selected
    df1= (DF.loc[DF['year_month'] == dt.today().strftime("%Y-%m")])

    #filtering rows with leaves=1
    df= (df1.loc[DF['leaves'] == 0])


    #droping unwanted columns
    df.drop(["leaves","year_month","id"], axis = 1, inplace = True)
    df.reset_index(drop=True, inplace=True)



    #returnig the dataframe as html table format
    return render_template("work.html",text= df.to_html())





#work_hours post page
@app.route("/WORK", methods=['POST'])
def works():

    #extracting the month submited
    r1=request.form["month"]

    #creating a dataframe(DF) from work table
    DF = pd.read_sql_table("work",URI)


    #creating new columns
    for n in range(len(DF.id)):
        DF["Employee Name"]="none"


    
    #adding values to column
    for n in range(len(DF.id)):
        DF["Employee Name"][n]=Work.query.filter_by(id= int(DF.id[n])).first().employee.name



    #creating new columns,and adding year_month to it
    DF["year_month"]=pd.to_datetime(DF.date).dt.to_period('M')

    #extracting the data with year_month selected
    df1= (DF.loc[DF['year_month'] == r1])

    #filtering rows with leaves=1
    df= (df1.loc[DF['leaves'] == 0])


    #droping unwanted columns
    df.drop(["leaves","year_month","id"], axis = 1, inplace = True)
    df.reset_index(drop=True, inplace=True)



    #returnig the dataframe as html table format
    return render_template("work.html",text= df.to_html())





#leave get page
@app.route("/LEAVES")

#login_required let the fuction execute only if user is loged in
@login_required
def leaves():


    #creating a dataframe(DF) from work table    
    DF = pd.read_sql_table("work",URI)


    #creating new columns
    for n in range(len(DF.id)):
        DF["Employee Name"]="none"


    #adding values to column
    for n in range(len(DF.id)):
        DF["Employee Name"][n]=Work.query.filter_by(id= int(DF.id[n])).first().employee.name



    #creating new columns,and adding year_month to it
    DF["year_month"]=pd.to_datetime(DF.date).dt.to_period('M')

    #extracting the data with year_month selected
    df1= (DF.loc[DF['year_month'] == dt.today().strftime("%Y-%m")])

    #filtering rows with leaves=1
    df= (df1.loc[DF['leaves'] == 1])


    #droping unwanted columns
    df.drop(["work_hours","year_month","id"], axis = 1, inplace = True)
    df.reset_index(drop=True, inplace=True)




    #returnig the dataframe as html table format
    return render_template("leaves.html",text= df.to_html())



#leave post page
@app.route("/LEAVES", methods=['POST'])
def leave():
    
    #extracting the month submited
    r1=request.form["month"]

    #creating a dataframe(DF) from work table    
    DF = pd.read_sql_table("work",URI)


    #creating new columns
    for n in range(len(DF.id)):
        DF["Employee Name"]="none"


    
    #adding values to column
    for n in range(len(DF.id)):
        DF["Employee Name"][n]=Work.query.filter_by(id= int(DF.id[n])).first().employee.name



    #creating new columns,and adding year_month to it
    DF["year_month"]=pd.to_datetime(DF.date).dt.to_period('M')

    #extracting the data with year_month selected
    df1= (DF.loc[DF['year_month'] == r1])

    #filtering rows with leaves=1
    df= (df1.loc[DF['leaves'] == 1])


    #droping unwanted columns
    df.drop(["work_hours","year_month","id"], axis = 1, inplace = True)
    df.reset_index(drop=True, inplace=True)



    
    #returnig the dataframe as html table format
    return render_template("leaves.html",text= df.to_html())


#logout page
@app.route("/LOGOUT")

#login_required let the fuction execute only if user is loged in
@login_required

def logout():

    #helps to logout user
    logout_user()
    return render_template("submit.html")



if __name__ == '__main__':
    app.debug=True
    app.run(port=5000)
