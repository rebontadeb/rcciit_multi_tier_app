from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
import os,json
import configparser
 
app = Flask('event-api')
parser = configparser.ConfigParser()
configFilePath = r'./config/app.config'
parser.read(configFilePath)

db_config = {
    'host': parser['database']['host'],
    'user': parser['database']['user'],
    'password': parser['database']['password'],
    'database': parser['database']['db'],
}



@app.route('/submit', methods=['POST']) #Insertion End-point
def submit_form():    
    jsonData = request.get_json()
    name = jsonData.get('name')
    email = jsonData.get('email')
    phone = jsonData.get('phone')
    gender = jsonData.get('gender')
    field = jsonData.get('field')
    stream = jsonData.get('stream')
    comments = jsonData.get('comments') 
    print(stream)
    db_conn = mysql.connector.connect(**db_config)       
    cursor = db_conn.cursor()
    insert_query = "INSERT INTO eventdata (name, email, phone, gender, field,comments,stream) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (name, email, phone, gender, field,comments,stream)
    cursor.execute(insert_query, data)
    db_conn.commit()
    cursor.close()
    jsonData = jsonify({'status': "success" })
    return jsonData



@app.route('/details',methods=['GET'])#Fetch End-point
def details():
    db_conn = mysql.connector.connect(**db_config)
    cursor = db_conn.cursor()
    select_query = "SELECT name, email, field, stream FROM eventdata"
    cursor.execute(select_query)
    data = cursor.fetchall()
    cursor.close()            
    jsonData = jsonify({'results': data})
    return jsonData

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=parser['app-api']['port'])

