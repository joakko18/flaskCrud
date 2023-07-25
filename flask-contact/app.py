from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
app = Flask(__name__)

#mysqlconnection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='4793960Jo.'
app.config['MYSQL_DB']='base2'
mysql = MySQL(app)

#session
app.secret_key= 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM newcontact')
    data =cur.fetchall()
    print(data)
    return render_template('index.html', newcontact=data)

@app.route('/addcontact',methods=['POST'])
def addContact():
    if request.method == 'POST':
        ID = request.form['ID']
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        print(ID)
        print(fullname)
        print(phone)
        print(email)
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO newcontact (ID,fullname,phone,email)VALUES(%s,%s,%s,%s)',(ID,fullname,phone,email))
        mysql.connection.commit()

        flash('Contact added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def editContact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM newcontact WHERE ID = %s',(id))
    data = cur.fetchall()
    print('edit')
    return render_template('edit.html',newcontact = data[0])

@app.route('/update/<id>',methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        ID = request.form['ID']
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE newcontact
        SET fullname = %s, phone = %s,email = %s where ID = %s""",
        (fullname,phone,email,ID))
    mysql.connection.commit()
    flash('contact updated succesfully')
    return redirect(url_for('Index'))

    

@app.route('/delete/<string:id>')
def deletecontact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM newcontact WHERE ID = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed succesfully')
    return redirect(url_for('Index'))

if __name__=='__main__':
 app.run(port = 3000, debug = True)