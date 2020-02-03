# ATTENDANCE APP

This app help for employees to submit the responose(employee_id) and save there response with time in a database, admin can login and find the total working hours and leaves for the selected month.

## Language
Python, HTML

## Framework
Flask

## Usage
* Edit the location of database by changing the database_uri value in config/cfg.ini
* Create a virtual python environment with virtual\Scripts\activate command in Command Prompt

    ```
    virtual\Scripts\activate
    ```

* run the run.py file in the virtual environment created

* open localhost/5000 in your browser

## Contents
### Submit page
Here the employee enters the employee id and stores the date &time in database

### Admin login page
Here the admin may submit his employee id with password to login and access work,leaves and admin page

### Admin Page
Here all data for all employees are visible

### Working HOURS
Here the total working hours for all employees are visible for the selected month, by default current monthdata will be visible

### Leaves
Here the total leaves for all employees are visible for the selected month,by default current monthdata will be visible

### Logout
this page helps admin to logout from current session

