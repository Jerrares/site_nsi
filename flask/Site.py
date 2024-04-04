from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
from pathlib import Path
app = Flask(__name__)

@app.route('/')
def accueil():
	Liste_salons = pd.read_csv('Salons.csv')
	data = Liste_salons["Test"]
	return render_template('Page_principale.html', data=data)

@app.route('/nouveaux_salons')
def nouveaux_salons():
    return render_template('ajouter_salon.html')



@app.route('/nouveau_salon',methods=['GET','POST'])
def nouveau_salon():
    salons = request.form.get("nom_salon")
    Liste_salons = pd.read_csv('Salons.csv')
    if "nom_salon" in Liste_salons:
        return render_template('ajouter_salon.html', message ="ce salon existe déja, veuillez donner un autre nom")
    nouvelle_ligne = pd.DataFrame([salons], columns=['Test'])
    Liste_salons = pd.concat([Liste_salons, nouvelle_ligne], ignore_index=True)
    Liste_salons.to_csv('Salons.csv')
    pd.DataFrame().to_csv('/salons/ 'f'{salons}.csv', index=False)
    return render_template('salon_réussit.html') 
    
'''
routes dynamiques en dessousq
'''


@app.route('/<ligne>')
def userlist(ligne):
	Liste_user = pd.read_csv(f'salons/{ligne}.csv')
	user = Liste_user[ligne]
	return render_template('Page_principale.html', data=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


app.run(debug=False, port=7000)
