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
    employee = cursor.fetchone() #取得欲請假的員工
    if employee: #檢測是否為空值
        employee = str(list(employee)[0]) #將員工名字從set中提取出來並轉型為string
        cursor.execute("SELECT name FROM employees") #取得全部員工名單
        response = list(cursor.fetchall()) #全體員工名單(set) ((a,),(b,),(c,))...
        employees = [] #代理人名單
        for i in response:
            for j in i:
                employees.append(j) #將set轉型為list
        employees.remove(employee) #從全體名單去除欲請假員工，避免選取自己作為代理人
        connection.close()
        session["employeeName"] = employee #儲存員工名字在session
        return render_template("leave.html",name=employee,employees=employees)
    else:
        connection.close()
        return render_template("errorIdNumber.html")

#leave requestion sended
@app.route("/sucess", methods=["post"])
def sucess():
    employName = session.get("employeeName") #欲請假員工姓名
    dateOfLeave = request.form["dateOfLeave"] #請假日期
    typeOfLeave = request.form["typeOfLeave"] #假別
    proof = request.files.get("proof") #證明文件檔
    agent = request.form["agent"] #代理人
    connection = sqlite3.connect("employees.db")
    cursor = connection.cursor()
    if proof: #檢測是否有證明文件，有則儲存至資料庫
        proofFile = proof.read()
        cursor.execute("INSERT INTO leave (name,date,type,proof,agent,verify) VALUES (?,?,?,?,?,?)",(employName,dateOfLeave,typeOfLeave,proofFile,agent,0,))
        connection.commit()
        connection.close()
    else: #若無則將其他資料儲存進資料庫
        cursor.execute("INSERT INTO leave (name,date,type,agent,verify) VALUES (?,?,?,?,?)",(employName,dateOfLeave,typeOfLeave,agent,0,))
        connection.commit()
        connection.close()
    return render_template("sucess.html")

if __name__ == "__main__":
    app.run()