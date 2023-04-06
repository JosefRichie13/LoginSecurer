import random
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

# Renders the Main Page
@app.route('/')
def mainPage():
    return render_template('Index.html')

# This generates a password based on a list of numbers, alphabets and symbols
@app.route('/genPassword', methods=['POST'])
def genPassword():
    generatedPasswordList = []
    numberList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    upperList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z"]
    lowerList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z"]
    symbolList = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]",
                  "|", ":", ";", "<", ">", "?"]

    lengthOfPwd = request.form['numberSelector']
    if lengthOfPwd == "15":
        generatedPasswordList.append(random.choices(numberList, k=4))
        generatedPasswordList.append(random.choices(upperList, k=4))
        generatedPasswordList.append(random.choices(lowerList, k=4))
        generatedPasswordList.append(random.choices(symbolList, k=3))
    elif lengthOfPwd == "16":
        generatedPasswordList.append(random.choices(numberList, k=4))
        generatedPasswordList.append(random.choices(upperList, k=4))
        generatedPasswordList.append(random.choices(lowerList, k=4))
        generatedPasswordList.append(random.choices(symbolList, k=4))
    elif lengthOfPwd == "17":
        generatedPasswordList.append(random.choices(numberList, k=4))
        generatedPasswordList.append(random.choices(upperList, k=4))
        generatedPasswordList.append(random.choices(lowerList, k=4))
        generatedPasswordList.append(random.choices(symbolList, k=5))
    elif lengthOfPwd == "18":
        generatedPasswordList.append(random.choices(numberList, k=4))
        generatedPasswordList.append(random.choices(upperList, k=4))
        generatedPasswordList.append(random.choices(lowerList, k=4))
        generatedPasswordList.append(random.choices(symbolList, k=6))
    elif lengthOfPwd == "19":
        generatedPasswordList.append(random.choices(numberList, k=4))
        generatedPasswordList.append(random.choices(upperList, k=4))
        generatedPasswordList.append(random.choices(lowerList, k=4))
        generatedPasswordList.append(random.choices(symbolList, k=7))
    elif lengthOfPwd == "20":
        generatedPasswordList.append(random.choices(numberList, k=4))
        generatedPasswordList.append(random.choices(upperList, k=4))
        generatedPasswordList.append(random.choices(lowerList, k=4))
        generatedPasswordList.append(random.choices(symbolList, k=8))

    genPwdList = [''.join(ele) for ele in generatedPasswordList]
    random.shuffle(genPwdList)
    generatedPasswordString = " ".join(genPwdList)
    generatedPasswordString = generatedPasswordString.replace(" ", "")

    return render_template('Index.html', TemplateGeneratedPassword=generatedPasswordString)

# This Stores the password in a DB
@app.route('/storePassword', methods=['POST'])
def storePassword():
    webpage = request.form['webpage']
    loginid = request.form['loginid']
    password = request.form['password']

    if webpage == "ADMIN":
        return render_template("Index.html", TemplateErrorMessage="ADMIN is not a Webpage, please enter a different name")

    values = "('" + webpage + "', '" + loginid + "', '" + password + "')"

    connection = sqlite3.connect("DB\\LoginSecurer.db")
    cur = connection.cursor()
    cur.execute("SELECT rowid FROM LOGINSECURER where WEBPAGE = '" + webpage + "';")
    usercheck = cur.fetchone()

    if usercheck is None:
        cur.execute("INSERT INTO LOGINSECURER (WEBPAGE, LOGINID, PASSWORD) VALUES " + values + ";")
        connection.commit()
        return render_template("Index.html", TemplateErrorMessage="Successfully stored login details for " + webpage)
    else:
        return render_template("Index.html", TemplateErrorMessage="Login for this Webpage, "+webpage+" already exists")

# This fetches the login details
@app.route('/getPassword', methods=['POST'])
def getPassword():
    webpage = request.form['getwebpage']
    adminkey = request.form['getkey']

    if webpage == "ADMIN":
        return render_template("Index.html", TemplatePasswordMessage="Cannot get the details for ADMIN user")

    connection = sqlite3.connect("DB\\LoginSecurer.db")
    cur = connection.cursor()

    cur.execute("SELECT rowid FROM LOGINSECURER where PASSWORD = '" + adminkey + "';")
    usercheck = cur.fetchone()
    if usercheck is None:
        return render_template("Index.html", TemplatePasswordMessage="Your Admin Key is wrong")


    cur.execute("SELECT rowid FROM LOGINSECURER where WEBPAGE = '" + webpage + "';")
    usercheck = cur.fetchone()

    if usercheck is None:
        return render_template("Index.html", TemplatePasswordMessage="No login details were found for this Webpage, " + webpage)
    else:
        cur.execute("SELECT * FROM LOGINSECURER where WEBPAGE = '" + webpage + "';")
        usercheck = cur.fetchone()
        return render_template("Index.html", TemplatePasswordMessage= "Your login details for " +webpage+ " are : "+ usercheck[1] +" and " + usercheck[2])

# Changes the Admin password
@app.route('/changeAdmin', methods=['POST'])
def changeAdmin():
    oldKey = request.form['oldKey']
    newKey = request.form['newKey']
    connection = sqlite3.connect("DB\\LoginSecurer.db")
    cur = connection.cursor()

    cur.execute("SELECT rowid FROM LOGINSECURER where PASSWORD = '" + oldKey + "';")
    usercheck = cur.fetchone()
    if usercheck is None:
        return render_template("Index.html", TemplateAdminMessage="Your old Admin Key is wrong")
    else:
        cur.execute("UPDATE LOGINSECURER SET PASSWORD = '"+newKey+"' where PASSWORD = '" + oldKey + "';")
        connection.commit()
        return render_template("Index.html", TemplateAdminMessage="New Key successfully updated")

# Deletes any login
@app.route('/deletePassword',  methods=['POST'])
def deletePassword():
    deletewebpage = request.form['deletewebpage']
    deleteadminkey = request.form['deletekey']

    if deletewebpage == "ADMIN":
        return render_template("Index.html", TemplatePasswordDeleted="Cannot delete the ADMIN user")

    connection = sqlite3.connect("DB\\LoginSecurer.db")
    cur = connection.cursor()

    cur.execute("SELECT rowid FROM LOGINSECURER where PASSWORD = '" + deleteadminkey + "';")
    usercheck = cur.fetchone()
    if usercheck is None:
        return render_template("Index.html", TemplatePasswordDeleted="Your Admin Key is wrong")

    cur.execute("SELECT rowid FROM LOGINSECURER where WEBPAGE = '" + deletewebpage + "';")
    usercheck = cur.fetchone()

    if usercheck is None:
        return render_template("Index.html", TemplatePasswordDeleted="No login details were found for this Webpage, " + deletewebpage)
    else:
        cur.execute("DELETE FROM LOGINSECURER where WEBPAGE = '" + deletewebpage + "';")
        connection.commit()
        return render_template("Index.html", TemplatePasswordDeleted= "Login details for " +deletewebpage+ " is deleted")



# Runs the App
if __name__ == '__main__':
    app.run(debug=True)
