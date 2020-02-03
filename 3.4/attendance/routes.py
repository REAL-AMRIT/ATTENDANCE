from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, url_for,redirect
from datetime import datetime as dt
from flask_babel import gettext

from attendance import db,URI,app
from attendance.functions1 import *
from attendance.lang import *




#submit page
@app.route("/")
def submit():

    return render_template('submit.html')




#sucess page
@app.route("/success", methods=['POST'])
def success():

    #extracting submit detail
    employee_id= request.form["employee_id"]
        
    try:
        return submit_page(employee_id)

    #check for all other error
    except Exception as e:
        db.session.rollback()
        return render_template("submit.html", text=e)





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

    try:
        return login_page(login_id,password)
        
    except Exception as e:
        return render_template("login.html", text=e)






#admin page
@app.route("/admin")

#login_required let the fuction execute only if user is loged in
@login_required
def admin():
    
    return render_template('admin.html',text=admin_page())






#work_hours get page
@app.route("/WORK")

#login_required let the fuction execute only if user is loged in
@login_required

def work():

    #extracting the month submited
    r1=dt.today().strftime("%Y-%m")

    #returnig the dataframe as html table format
    return render_template("work.html",text= data_work(r1,URI))







#work_hours post page
@app.route("/WORK", methods=['POST'])
def works():

    #extracting the month submited
    r1=request.form["month"]

    #returnig the dataframe as html table format
    return render_template("work.html",text= data_work(r1,URI))





#leave get page
@app.route("/LEAVES")

#login_required let the fuction execute only if user is loged in
@login_required
def leaves():

    r1=dt.today().strftime("%Y-%m")


    #returnig the dataframe as html table format
    return render_template("leaves.html",text=data_leave(r1,URI))





#leave post page
@app.route("/LEAVES", methods=['POST'])
def leave():
 
    #extracting the month submited
    r1=request.form["month"]

    #returnig the dataframe as html table format
    return render_template("leaves.html",text=data_leave(r1,URI))






#logout page
@app.route("/LOGOUT")

#login_required let the fuction execute only if user is loged in
@login_required

def logout():

    #helps to logout user
    logout_user()
    return render_template("submit.html")