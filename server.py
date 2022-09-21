import uuid
from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__, template_folder='template')

app.secret_key = 'Tahve bqltuyej tbrjereq qobfd MvIaTq cmanmvpcuxsz iesh tihkel CnTu dretpyauritompeanstd '
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'intern_portal'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    returner = {}
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT * FROM account WHERE email = "{email}" AND password = "{password}"')
    account = cursor.fetchone()
    if account:
        name = account['name']
        session['loggedin'] = True
        session['email'] = account['email']
        session['utype']=account['usertype']
        # session['id'] = account['id']
        session['username'] = account['name']
        returner['status']="login success"
        returner['utype']=session['utype']
        return render_template('index.html',utype=account['usertype'],uname =name.upper())
    else:
        return render_template('error.html',error = "Invalid username/ password")
@app.route('/logout', methods=['POST'])
def logout():
   returner = {}
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('username',None)
   session.pop('utype', None)
   returner['status']="logout success"
   return render_template("login.html")

@app.route('/index',methods=['POST','get'])
def index():
    return render_template("index.html")

@app.route('/dashboard',methods=['Post'])
def dashboard():
    return 
@app.route('/course',methods=['POST'])
def course():
    id = session['id']
    if id:
        query= f"select i.empid,i.status,c.name,c.duration, form intern_course i,course c where i.courseid = c.courseid and i.empid = {id}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        coursedetails = cursor.fetchall()
        return coursedetails
    else:
        return render_template("error.html","Oops Something Went Wrong")

@app.route('/feedback',methods=['POST'])
def feedback():
    id = session['id']
    if id:
        query = f"select * from feedback where reciverId = {id}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        feedbackdetails = cursor.fetchall()
        return feedbackdetails
    else:
        return render_template("error.html","Oops Something Went Wrong")

@app.route('/sendfeedback',methods=['POST'])
def send():
    recieverId = session['id']
    senderId = request.form['sId']
    comment = request.form['comment']
    feedbackid = uuid.uuid1()
    if recieverId and senderId and comment and feedbackid:
        query = f"Insert into feedback values({feedbackid},'{senderId}','{recieverId}','{comment}')"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return redirect('index.html')
    else:
        return redirect('error.html',"Something went wrong")

@app.route('/project',methods=['POST'])
def projects():
    internId = session['id']
    if internId:
        query = f"select * from projects where internid = {internId}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        projectsdetails = cursor.fecthall()
        return redirect('index.html',projectsdetails)
    else:
        return redirect('error.html',"Something went wrong")
@app.route('/mproject',methods=['POST'])
def mprojects():
    id = session['id']
    if id:
        query = f"select * from projects where managerid = {id}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        projectsdetails = cursor.fecthall()
        return redirect('index.html',projectsdetails)
    else:
        return redirect('error.html',"Something went wrong")

@app.route('/interndetail',methods=['post'])
def interndetails():
    id = session['id']
    if id:
        query = f"select * from intern_manager where managerid = {id}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        interndetails = cursor.fecthall()
        return redirect('index.html',interndetails)
    else:
        return redirect('error.html',"Something went wrong")




if __name__== "__main__":
    app.run(debug=True)
