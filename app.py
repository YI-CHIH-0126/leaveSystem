from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
import initSQL
import config
app = Flask(__name__)
app.config.from_pyfile("config.py") #引入一個儲存不適合放上github的資料(api_key等)

#set sql
initSQL.setUpSQL()

#sign in page
@app.route("/")
def index():
    return render_template("index.html")

#ask leave page
@app.route("/leave", methods=["post"])
def leave():
    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees WHERE idNumber = ?",(request.form["idNumber"],)) #get()會返回元組，form["idNumber"]則會返回字串
    employee = cursor.fetchone()
    if employee:
        connection.close()
        session["employeeName"] = employee[1]
        return render_template("leave.html",name=employee[1])
    else:
        connection.close()
        return render_template("errorIdNumber.html")

#leave requestion sended
@app.route("/sucess", methods=["post"])
def sucess():
    employName = session.get("employeeName")
    dateOfLeave = request.form["dateOfLeave"]
    typeOfLeave = request.form["typeOfLeave"]
    proof = request.files.get("proof")
    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()
    if proof:
        proofFile = proof.read()
        cursor.execute("INSERT INTO leave (name,date,type,proof) VALUES (?,?,?,?)",(employName,dateOfLeave,typeOfLeave,proofFile,))
        connection.commit()
        connection.close()
    else:
        cursor.execute("INSERT INTO leave (name,date,type) VALUES (?,?,?)",(employName,dateOfLeave,typeOfLeave,))
        connection.commit()
        connection.close()
    return render_template("sucess.html")

if __name__ == "__main__":
    app.run()