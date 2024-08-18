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
    cursor.execute("SELECT name FROM employees WHERE idNumber = ?",(request.form["idNumber"],)) #get()會返回元組，form["idNumber"]則會返回字串
    employee = cursor.fetchone()
    if employee:
        employee = str(list(employee)[0])
        cursor.execute("SELECT name FROM employees")
        response = list(cursor.fetchall())
        employees = []
        for i in response:
            for j in i:
                employees.append(j)
        employees.remove(employee)
        connection.close()
        session["employeeName"] = employee
        return render_template("leave.html",name=employee,employees=employees)
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
    agent = request.form["agent"]
    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()
    if proof:
        proofFile = proof.read()
        cursor.execute("INSERT INTO leave (name,date,type,proof,agent,verify) VALUES (?,?,?,?,?,?)",(employName,dateOfLeave,typeOfLeave,proofFile,agent,0,))
        connection.commit()
        connection.close()
    else:
        cursor.execute("INSERT INTO leave (name,date,type,agent,verify) VALUES (?,?,?,?,?)",(employName,dateOfLeave,typeOfLeave,agent,0,))
        connection.commit()
        connection.close()
    return render_template("sucess.html")

if __name__ == "__main__":
    app.run()