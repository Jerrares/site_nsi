from flask import Flask, render_template, request, make_response, redirect, session
from flask_socketio import SocketIO, emit
from flask_session import Session
import pandas as pd # on importe pandas pour pouvoir lire les fichier csv                                 
from pathlib import Path
import secrets as sc
import NSI
'''
Au dessus les différentes librairies python que nous utiliserons sont importés, on a:
Flask pour la gestion du serveur
flask_socketio, un module qui va permettre de gerer un chat en temps réel
pandas pour la gestion de nos csv
'''


app = Flask(__name__) # ici on cree un serveur avec flask
app.config['SESSION_TYPE'] = 'filesystem' #ici avec le module flask_session on fait en sortes que les données ne soient pas stockés dans des cookies mais dans les fichiers du serveurs 
app.config['SECRET_KEY'] = "j'en ai ras le cul"










@app.route('/')
def connecté():

    if 'user' in session:#ici on vérifie que l'utilisateur est déja venu sur notre site web et que ses informations sont bien stockés dans nos données dans session
        return redirect('/accueil')# si c'est le cas on le redirige vers la page d'accueil

    return redirect('/connexion')#sinon on le redirige vers la page de connexion









@app.route('/accueil')
def accueil():

    total, salons = NSI.liste_salons()#En utilisant la fonction crée dans NSI.py nous récupérons le nombre de salons ainsi qu'une liste de dictionnaires qui les contiens 

    return render_template('accueil.html', salons=salons)#on affiche la page d'accueil a laquel on fourni notre liste des salons sous forme de dictionnaire








@app.route('/connexion', methods=['GET', 'POST'])#ici on spécifie que l'on peut recevoir mais aussi envoyer des donnés 
def login():

    error = '' #on initialise la variable error que l'on utilisera plus tard  

    if request.method == 'POST': #pour éviter tout problème on vérifie que l'utilisateur a soumis son formulaire de connexion

        pseudo = request.form['pseudo'] #on récupère la valleur de pseudo donné dans le html
        if len(pseudo) > 3 :#ici on vérifie que le pseudo soumis fait bien plus de 3 caractères

            utilisateur = NSI.nouvel_utilisateur(pseudo)#grace a une fonction du fichier NSI.py on rempli la variable utilisateur avec un tableau contennant son pseudo ainsi que son id

            if utilisateur is not None:    #on vérifie que l'utilisateur n'éxiste pas déja 
                session['user'] = utilisateur #on stocke l'utilisateur dans nos données interne pour pouvoir sauvegarder les informations le concernant 
                return redirect('/accueil') #on le redirige vers la page d'accueil

            else:
                error = 'Ce pseudo est déja utilisé!' #on a détécté une erreur donc on indique le le pseudo est déja utilisé

        else:
            error = "Ce pseudo n'est pas valide"#on a détécté une erreur donc on indique le le pseudo n'est pas valide


    return render_template('connexion.html', error=error)# on réaffiche donc la page de connexion en lui donnant la variable error pour qu'elle puisse être affiché dans la fenetre de connexion 
    








@app.route('/déconexion', methods=['GET'])#ici on spécifie que l'on va recevoir des donnés
def logout():

    id = session['user']['id']#on récupère l'id de l'utilisateur et on le stocke dans la variable id
    NSI.supression_utilisateur(id)#on suprime l'utilisateur en utilisant une fonction de NSI.py
    session.pop('user')#on suprime donc cet utilisateurs des données que l'on sauvegardes sur les utilisaturs

    return redirect('/connexion')#on redirige l'utilsateur qui n'as plus de compte vers la page de connexion











@app.route('/nouveau_salon', methods=['GET', 'POST'])#ici on spécifie que l'on peut recevoir mais aussi envoyer des donnés
def new_room():

    error = '' #on initialise la variable error que l'on utilisera plus tard

    if request.method == 'POST':#pour éviter tout problème on vérifie que l'utilisateur a soumis son formulaire de connexion

        nom_salon = request.form['salon']#on récupère la valleur de pseudo donné dans le html
        if len(nom_salon) > 3:#ici on vérifie que le nom du salon soumis fait bien plus de 3 caractères

            nouveau_salon = NSI.création_salon(nom_salon, session['user'])#grace a une fonction du fichier NSI.py on rempli la variable nouveau_salon avec un tableau contennant son pseudo ainsi que son i
            return redirect('/accueil')#une fois le nouveau salon crée on redirige l'utilisateur vers la page d'accueil

        else:
            error = "le nom n'est pas valide"#si le nom du salon n'est pas valide on remplie la variable d'erreur

    return render_template('nouveau_salon.html', error=error)#et donc en cas d'erreur on remet la page de création de salon en ajoutant le message d'erreur












@app.errorhandler(404)
def page_not_found(error):# ici la fonction permet de gérer les erreurs 404 
    return render_template('404.html')






@app.errorhandler(500)
def cttcasé(error):
    return render_template('cassé.html')





