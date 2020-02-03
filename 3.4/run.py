"""Web App for storing working hours, leaves,attendence
CURENT datetime"""


#this file helps to run the pakage



from attendance import app




if __name__ == '__main__':
    app.debug=True
    app.run(port=5000)
