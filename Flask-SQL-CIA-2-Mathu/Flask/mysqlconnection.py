from flask import Flask, render_template, request, redirect, url_for,session
import pymysql
import pickle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)
app.secret_key = 'super secret key'



HOST = 'localhost'
USER = 'root'
PASSWORD = '***************'
DB_NAME = 'sys'


wsgi_app = app.wsgi_app

@app.route('/')
def Home():
   
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html') 

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print("Here-0")
        username = request.form['username']
        password = request.form['password']
        connection = pymysql.connect(host='localhost', user='root', password=PASSWORD, database=DB_NAME )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Flaskmodel WHERE Name =%s AND Pswd=%s',(username,password))
        user = cursor.fetchone()
        
    

        if user:
            print("Here-1")
            return render_template('index.html')
        else:
            print("Err")
            error = 'Invalid username or password'
            return render_template('home.html')
    print("Callback-1")
    return render_template('home.html')





@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':

        print("inside predict function")
        class1 = int(request.form['Ticket Class'])
        sex = str(request.form['Sex'])
        age = float(request.form['Age'])
        sibsp = int(request.form['Number of Siblings/Spouse'])
        parch = int(request.form['Number of Parents/Children'])
        embark = float(request.form['Port of Embarkation'])

        if sex == 'Female':
            gender = 1
        if sex == 'Male':
            gender =0


        values = [class1,gender,age,sibsp,parch,embark]

        result = model.predict([values])

        if (result==0):
            result = 'dead'
        if (result==1):
            result = 'alive'
        

        return render_template('result.html', result=result)
    
    print("Yes")
    
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
