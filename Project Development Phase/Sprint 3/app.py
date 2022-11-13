import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template,redirect,url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.python.keras.backend import set_session
app=Flask(__name__)
model=load_model('vegetable.h5')
model1=load_model('fruit.h5')
#home page
@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/prediction')
def prediction():
	return render_template('predict.html')
@app.route('/predict',methods=['POST','GET'])
def predict():
	if(request.method=='POST'):
		f=request.files['image']
		basepath=os.path.dirname(__file__)
		file_path=os.path.join(basepath,'',secure_filename(f.filename))
		#print(file_path)
		f.save(file_path)
		img=image.load_img(file_path,target_size=(128,128))
		x=image.img_to_array(img)
		x=np.expand_dims(x,axis=0)
		plant=request.form['plant']
		print(plant)
		if(plant=='Vegetable'):
			preds=model.predict(x)
			print(preds)
			df=pd.read_excel('precautions-veg.xlsx')
			print(df.iloc[preds[0]]['caution'])
		else:
			preds=model1.predict(x)
			print("name=",preds[0])
			df=pd.read_excel('precautions-fruits.xlsx')
			#print(df.iloc[preds[0]]['caution'])
		return render_template("predicted.html",disease=str(df.iloc[np.where(preds[0]==1)[0][0]]['disease_name']),data=str(df.iloc[np.where(preds[0]==1)[0][0]]['caution']))
        
if(__name__=="__main__"):
	app.run(debug=True)