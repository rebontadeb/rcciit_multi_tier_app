from flask import Flask, render_template, request, redirect, url_for
import requests,urllib,json
import configparser

app = Flask('testapp', template_folder='./src/templates', static_folder='./src/static')
parser = configparser.ConfigParser()
configFilePath = r'./config/app.config'
parser.read(configFilePath)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    field = request.form['perform']
    stream = request.form['stream']
    comments = request.form['comments']  
      
    input_data = {"name":name,"email":email,"phone": phone, "gender": gender, "field": field,"stream":stream,"comments": comments}
    url = "http://"+parser['app-api']['host']+":"+parser['app-api']['port']+"/submit"
    headers = {'Content-Type': 'application/json'}       
    jsondata = json.dumps(input_data).encode("utf-8")
    response =  requests.post(url, data=jsondata, headers=headers)    
    return redirect(url_for('interstitial'))

@app.route('/interstitial')
def interstitial():
    return render_template('interstitial.html')

@app.route('/details')
def details():
    url = "http://"+parser['app-api']['host']+":"+parser['app-api']['port']+"/details"
    response = urllib.request.urlopen(url)
    data = response.read()
    jsondata = json.loads(data)
    return render_template('details.html', data=jsondata["results"])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=parser['app-gui']['port'])

