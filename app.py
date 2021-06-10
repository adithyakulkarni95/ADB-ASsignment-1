from flask import Flask, render_template, request, redirect, url_for, flash, Request
import pandas as pd
import csv
import numpy as np
import os
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="ABCDEF"

path="./people.csv"
tempPath="./new.csv"
UPLOAD_FOLDER = 'static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
fieldnames=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords']

df = pd.read_csv('people.csv')
df1=df.replace(np.nan,"",regex=True)
data = df1.values.tolist()
Name=""

@app.route('/', methods=["POST","GET"])
def hello():
	return render_template('index.html')

@app.route('/homepage', methods=["POST","GET"])
def home():
	return render_template('index.html')

@app.route('/everyone',methods=["POST","GET"])
def search():	
	df = pd.read_csv('people.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	return render_template('everyone.html',dict=data)

@app.route('/searchdata',methods=["POST","GET"])
def searchdata():
	df = pd.read_csv('people.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	name = request.form.get("SearchBar")
	return render_template('search.html',dict=data, name=name)
	
@app.route('/salary',methods=["POST","GET"])
def saldata():
	df = pd.read_csv('people.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	people = []
	salary = request.form.get("salBar")
	salary = float(salary)
	for items in data:
		salary = 0
		if(items[2] != "" and items[2] != " "):
			salary1 = float(items[2])
		if (salary<salary1):
			people.append(items)
	return render_template('salary.html',dict=people, sal=salary)


@app.route('/showdetails', methods=["POST","GET"])
def show():
	name = request.form.get("SearchBar")
	global Name
	Name=name
	print(Name)
	df = pd.read_csv('people.csv')
	df1=df.replace(np.nan,"",regex=True)
	data = df1.values.tolist()
	return render_template('update.html',dict=data, name=name)


@app.route('/update',methods=["POST","GET"])
def updatedata():	
	name = request.form.get("name")
	state = request.form.get("state")
	salary = request.form.get("salary")
	grade = request.form.get("grade")
	room = request.form.get("room")
	telnum = request.form.get("telnum")
	keywords = request.form.get("keywords")
	with open(tempPath, mode='w') as csv_file:
		linewriter=csv.writer(csv_file)
		mywriter=csv.DictWriter(csv_file,fieldnames=fieldnames)
		mywriter.writeheader()
		with open(path, mode='r') as csv_file:
			myreader = csv.DictReader(csv_file)
			for row in myreader:
				if row['Name']==name:
					print(row)
					if(request.form['update'] == 'Update'):
						linewriter.writerow([name,state,salary,grade,room,telnum,row['Picture'],keywords])
					else:
						continue
				else:
					mywriter.writerow(row)
	os.remove(path)
	os.rename(tempPath,path)
	return redirect(url_for('home'))


@app.route('/uploadimage',methods=["POST"])
def uploadimg():
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			tempPath="./new.csv"
			with open(tempPath, mode='w') as csv_file:
				linewriter=csv.writer(csv_file)
				mywriter=csv.DictWriter(csv_file,fieldnames=fieldnames)
				mywriter.writeheader()
				with open(path, mode='r') as csv_file:
					myreader = csv.DictReader(csv_file)
					for row in myreader:
						if row['Name']==Name:
							print(row)
							linewriter.writerow([row['Name'],row['State'],row['Salary'],row['Grade'],row['Room'],row['Telnum'],filename,row['Keywords']])
						else:
							mywriter.writerow(row)
			os.remove(path)
			os.rename(tempPath,path)
			return redirect(url_for('home'))
		else:
			flash('Allowed images types are - png, jpg, jpeg, gif')
			return redirect(url_for('home'))

if __name__ == '__main__':
    
  app.run(host='127.0.0.1', port=8080, debug=True)
  app.config['JSON_SORT_KEYS']=False
