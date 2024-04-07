from flask import Flask#ici on importe flask et les differente bibliothèques python.
from flask_socketio import SocketIO
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from flask_socketio import emit
import os
import pandas as pd # on importe pandas pour pouvoir lire les fichier csv                                 
from pathlib import Path
import secrets as sc
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def test():
    token = request.cookies.get('token')
    token_pseudo = pd.read_csv('data/token/token_pseudo.csv')
    if token in token_pseudo:
        return redirect('/accueil')
    return render_template('connexion.html'), token

@app.route('/connect')
def connexions():
    return render_template('connexion.html')

@app.route('/connexion', methods=['GET','POST'])
def connexion():
    token = sc.token_hex(62)
    cookie = make_response(render_template('Page_principale.html'))
    cookie.set_cookie('token', token, max_age=3650*24*3600)
    print(token)
    token_pseudo = pd.read_csv('data/token/token_pseudo.csv')
    if token in token_pseudo:
        token_pseudo = token_pseudo.drop(token)
    pseudo = request.form.get("pseudo")
    print(pseudo)
    token_pseudo[token] = pseudo
    token_pseudo.to_csv('data/token/token_pseudo.csv')
    return cookie

@app.route('/accueil')
def accueil():# cette fonction permet d'extraire une collone avec ses donnees
	Liste_salons = pd.read_csv('Salons.csv')# et de les affiches dans une page web 
	data = Liste_salons["Test"]
	return render_template('Page_principale.html', data=data)

@app.route('/nouveaux_salons')
def nouveaux_salons():# la fonction nouveau salon permet de à générer une page web 
    return render_template('ajouter_salon.html')# à partir d'un template HTML nommé ajouter_salon.html



@app.route('/nouveau_salon',methods=['GET','POST'])						  
def nouveau_salon():
    nom_salon = request.form.get("nom_salon")# La fonction commence par récupérer le nom du salon soumis par l'utilisateur via le formulaire 
    Liste_salons = pd.read_csv('Salons.csv')# Ensuite, la fonction lit le fichier CSV Salons.csv en utilisant la bibliothèque Pandas							   
    if nom_salon in Liste_salons: # La fonction vérifie ensuite si le nom du salon soumis par l'utilisateur existe déjà                                                              
        return render_template('ajouter_salon.html', message ="ce salon existe déja, veuillez donner un autre nom")# si le salon existe deja le site renvoie un message d'erreur "veuillez donner un autre nom".
    nouveau_salon = pd.DataFrame([[nom_salon]], columns=['Test'] )
    Liste_salons = pd.concat([Liste_salons,nouveau_salon], ignore_index=False)# ce code permet d'ajouter un nouveau salon à une liste de salons stockée dans un fichier CSV, 
    Liste_salons.to_csv('Salons.csv')
    vide = pd.DataFrame({"Test":[]})# de créer un fichier CSV spécifique pour le nouveau salon,
    vide.to_csv(f'data/{nom_salon}.csv', index=False)# et d'informer l'utilisateur que l'opération a réussi
    os.makedirs(f'data/{nom_salon}')
    return render_template('salon_réussit.html')
        
    '''
    routes dynamiques en dessous
    '''
    
    
@app.route('/<ligne>')
def userlist(ligne):
    Liste_user = pd.read_csv(f'data/{ligne}.csv')
    token = request.cookies.get('token')
    utilisateurs = pd.DataFrame([[token]], columns=['Test'] )
    Liste_user = pd.concat([Liste_user,utilisateurs], ignore_index=False)# ce code permet d'ajouter un nouveau salon à une liste de salons stockée dans un fichier CSV, 
    Liste_user.to_csv(f'data/{ligne}.csv')# Cette ligne utilise la bibliothèque Pandas pour lire un fichier CSV situé dans le dossier salons
    user = Liste_user['Test']# Cette ligne extrait une colonne spécifique du DataFrame Pandas créé à partir du fichier CSV
    vide = pd.DataFrame({"id":[],"utilisateurs":[]})
    vide.to_csv(f'data/{ligne}/base_fonctionel.csv', index=False)
    return render_template('page_utilisateurs.html', data=user, ligne=ligne)# Cette ligne génère une réponse HTML à partir du template
    
    
@app.route('/<ligne>/<user>')
def chat(user,ligne):
    base_fonctionel = pd.read_csv(f'data/{ligne}/base_fonctionel.csv')
    user1 = request.cookies.get('token')
    user2 = user
    if user1 in base_fonctionel and user in base_fonctionel:
        if base_fonctionel[user1] == base_fonctionel[user]:
            id = base_fonctionel[user1]
            return redirect(f'/discussion/{id}')
    id = sc.token_hex(12)
    base_fonctionel1 = pd.DataFrame([[id, user1]], columns=["id","utilisateurs"])
    base_fonctionel2 = pd.DataFrame([[id, user2]], columns=["id","utilisateurs"])
    base_fonctionel = pd.concat([base_fonctionel, base_fonctionel1, base_fonctionel2], ignore_index=False)
    base_fonctionel.to_csv(f'data/{ligne}/base_fonctionel.csv')
    return redirect(f'/discussion/{id}')



@app.route('/discussion/<id>')
def discussion(id):
    return render_template("chat.html", id=id)
    
    
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    emit('message', data, broadcast=True)
    




    

@app.errorhandler(404)
def page_not_found(error):# ici la fonction permet de gérer les erreurs 404 
    return render_template('404.html')

@app.errorhandler(500)
def cttcasé(error):
    return render_template('cassé.html')

if __name__ == '__main__':
    socketio.run(app)

