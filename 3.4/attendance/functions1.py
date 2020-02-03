import pandas as pd   
from flask_babel import gettext
from flask import  render_template, request, url_for,redirect
from datetime import datetime as dt
from flask_login import login_user, login_required, current_user


from attendance.models import Employee,Role,User,Department,Attendance,Holidays,Work
from attendance import URI,db
from attendance.lang import *





def submit_page(employee_id):
    



        emp= Employee.query.all()
        

        #checking if the current day is saturday or not, strftime('%A') returns day in string format
        if dt.now().strftime('%A')!="Saturday" and dt.now().strftime('%A')!= "Sunday":
            for i in emp:

                #checking if curent date is in holidays table, adding leaves for all employess for current date if condition is satisfied
                if Work.query.filter_by(date=dt.now().date(), employee_id= i.id).count() != 1 and Holidays.query.filter_by(date=dt.now().date()).count() !=1 :
                    data= Work(date= dt.now(),leaves= 1, employee_id=i.id)
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
            data= Attendance(employee_id=employee_id,in_out=inout,DT= dt.now())
            db.session.add(data)
            db.session.commit()
            
            
            #extracting the last signin entry of current employee
            data1=Attendance.query.filter_by(employee_id=employee_id, in_out= "in")[-1]
            
        
            #converting the datetime format to string time forma
            hour1=data1.DT.strftime("%H:%M:%S")
            hour11=data1.DT.strftime("%I:%M:%S %p")

            
            #converting the datetime format to date format
            day = data.DT.date()
            
            if data.in_out == "in":           

                return render_template("submit.html", text= gettext(sign_in) + "  at " + ":   "+ hour11)

            elif data.in_out=="out":
                hour2 = data.DT.strftime("%H:%M:%S")
                hour22 = data.DT.strftime("%I:%M:%S  %p")
                
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
                else:
                    pass

            else:
                pass

            return render_template("submit.html", text= gettext(sign_out)+ "  " + ":   "+ hour22)
        else:
            return render_template("submit.html", text=gettext(wrong_id))
    



def login_page(login_id,password):


    #filtering emploee row from employee table
    employe1=Employee.query.filter_by(id= login_id).first()
    if employe1:
        #checking the login details from user and employee table
        
        if employe1.user.user_type== "admin"  and employe1.user.password == password:
            

            #Creates a cookie with user id
            login_user(employe1)

            return redirect(url_for('admin'))
    else:
        return render_template("login.html",text=gettext(login_details))






#display total leave for selected month
def data_leave(r1,URI):


    try:
        #creating a dataframe(DF) from work table
        DF = pd.read_sql_table("work",URI)
        DF1= pd.read_sql_table("employee",URI)
        #creating new columns,and adding year_month to it
        DF["year_month"]=pd.to_datetime(DF.date).dt.to_period('M')

        #extracting the data with year_month selected
        df1= (DF.loc[DF['year_month'] == r1])

        #filtering rows with leaves=1
        df= (df1.loc[DF['leaves'] == 1])

        if df["leaves"].count() != 0:

            #finding totalleave for given the month
            
            data= df.groupby('employee_id')['leaves'].sum().reset_index()

            for n in range(len(data.employee_id)):
                data["Employee Name"]="none"


            #adding values to column
            for n in range(len(data.employee_id)):
                data["Employee Name"][n]=DF1.loc[DF1['id'] == data["employee_id"][n],"name"].values[0]


            column_titles = ["employee_id","Employee Name","leaves"]

            data=data.reindex(columns=column_titles)

            return data.to_html()
        else:
            return gettext(invalid_data)

    except Exception as e:
        return e





#display total leave for selected month
def data_work(r1,URI):
    
    try:

        #creating a dataframe(DF) from work table
        DF = pd.read_sql_table("work",URI)
        DF1= pd.read_sql_table("employee",URI)

        #creating new columns,and adding year_month to it
        DF["year_month"]=pd.to_datetime(DF.date).dt.to_period('M')

        #extracting the data with year_month selected
        df1= (DF.loc[DF['year_month'] == r1])

        #filtering rows with leaves=1
        df= (df1.loc[DF['leaves'] == 0])
        df.reset_index(drop=True, inplace=True)

        if df["leaves"].count() != 0:

            #finding total time for given the month

            def parse_time(s):
                hour, min, sec = s.split(':')
                try:
                    hour = int(hour)
                    min = int(min)
                    sec = int(sec)
                except ValueError:
                    # handle errors here, but this isn't a bad default to ignore errors
                    return 0
                return hour * 60 * 60 + min * 60 + sec



            d=0
            d1=[]

            for i in df.work_hours:

                i=i.strftime("%H:%M:%S")
                d+= parse_time(i)
                d1.append(parse_time(i))
                df["seconds"]="none"

            for i in range(len(d1)):
                df["seconds"][i]=int(d1[i])


        
            data= df.groupby('employee_id')['seconds'].sum().reset_index()

            for n in range(len(data.employee_id)):
                data["Employee Name"]="none"

            #adding values to column
            for n in range(len(data.employee_id)):
                data["Employee Name"][n]=DF1.loc[DF1['id'] == data["employee_id"][n],"name"].values[0]



            data["m"]=round(data["seconds"]/60)
            data["hours"]=round(data["m"]/60)
            data["minutes"]=round(data["m"]%60)
            data["sec"]= round(data["seconds"]%60)

            data["time"] = data.hours.map(str) + " hours, " + data.minutes.map(str)+ " minutes,  " + data.sec.map(str)+ " sec"



            #droping unwanted columns
            data.drop(["hours","minutes","m","seconds"], axis = 1, inplace = True)

            return data.to_html()
        else:
            return gettext(invalid_data)
    
    except Exception as e:
        return e



#display employees details
def admin_page():


    try:

        
        #creating a dataframe from employee table
        data = pd.read_sql_table("employee",URI,index_col=False)


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

        return data.to_html()

    except Exception as e:
        return e