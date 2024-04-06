from flask import Flask                             						   #ici on importe flask et les differente bibliothèques python.  
from flask import render_template
from flask import request
import pandas as pd                                					           # on importe panda pour pouvoir lire les fichier csv                                 
from pathlib import Path
app = Flask(__name__)

@app.route('/')
def accueil():                                                                                     # cette fonction permet d'extraire une collone avec ses donnees
	Liste_salons = pd.read_csv('Salons.csv')						   # et de les affiches dans une page web 
	data = Liste_salons["Test"]
	return render_template('Page_principale.html', data=data)

@app.route('/nouveaux_salons')
def nouveaux_salons():										  # la fonction nouveau salon permet de à générer une page web 
    return render_template('ajouter_salon.html')						  # à partir d'un template HTML nommé ajouter_salon.html



@app.route('/nouveau_salon',methods=['GET','POST'])						  
def nouveau_salon():										  # La fonction commence par récupérer le nom du salon soumis par l'utilisateur via le formulaire
    nom_salon = request.form.get("nom_salon")
    print(nom_salon)# Ensuite, la fonction lit le fichier CSV Salons.csv en utilisant la bibliothèque Pandas 
    Liste_salons = pd.read_csv('Salons.csv')							  # La fonction vérifie ensuite si le nom du salon soumis par l'utilisateur existe déjà 
    if nom_salon in Liste_salons:                                                               # si le salon existe deja le site renvoie un message d'erreur "veuillez donner un autre nom".
        return render_template('ajouter_salon.html', message ="ce salon existe déja, veuillez donner un autre nom")
    nouveau_salon = pd.DataFrame([[nom_salon]], columns=['Test'] )
    Liste_salons = pd.concat([Liste_salons,nouveau_salon], ignore_index=False)               # ce code permet d'ajouter un nouveau salon à une liste de salons stockée dans un fichier CSV, 
    Liste_salons.to_csv('Salons.csv')
    vide = pd.DataFrame({"Test":[]})# de créer un fichier CSV spécifique pour le nouveau salon,
    vide.to_csv(f'salons/{nom_salon}.csv', index=False)				  # et d'informer l'utilisateur que l'opération a réussi 
    return render_template('salon_réussit.html') 
    
'''
routes dynamiques en dessous
'''


@app.route('/<ligne>')
def userlist(ligne):
    Liste_user = pd.read_csv(f'salons/{ligne}.csv')
    adresses_ip = request.remote_addr
    utilisateurs = pd.DataFrame([[adresses_ip]], columns=['Test'] )
    Liste_user = pd.concat([Liste_user,utilisateurs], ignore_index=False)               # ce code permet d'ajouter un nouveau salon à une liste de salons stockée dans un fichier CSV, 
    Liste_user.to_csv(f'{ligne}.csv')    		 			  # Cette ligne utilise la bibliothèque Pandas pour lire un fichier CSV situé dans le dossier salons
    user = Liste_user['Test']								  # Cette ligne extrait une colonne spécifique du DataFrame Pandas créé à partir du fichier CSV
    return render_template('page_utilisateurs.html', data=user)				  # Cette ligne génère une réponse HTML à partir du template

@app.errorhandler(404)
def page_not_found():										  # ici la fonction permet de gérer les erreurs 404 
    return render_template('404.html')

@app.errorhandler(500)
def cttcasé(error):
    return render_template('cassé.html')


