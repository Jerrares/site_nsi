from flask import Flask, render_template, request, make_response, redirect, session
from flask_socketio import SocketIO, emit
from flask_session import Session
import pandas as pd # Importe pandas pour lire les fichiers CSV
from pathlib import Path
import secrets as sc
import NSI # Importe le module NSI pour accéder à ses fonctions

# Initialise Flask et configure les sessions pour utiliser le système de fichiers
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem' # Les données de session sont stockées dans des fichiers sur le serveur
app.config['SECRET_KEY'] = "hjbpjbgvgoujbhvgoujvjgg" # Clé secrète pour la sécurité des sessions
socketIO = SocketIO(app) # Initialise SocketIO pour la communication en temps réel

@app.route('/')
def connecté():
    """
    >>> from flask import session
    >>> session['user'] = {'id': 1}
    >>> connecté()
    <Response 302>
    """
# Vérifie si l'utilisateur est déjà connecté
    if 'user' in session:
        return redirect('/accueil') # Redirige vers la page d'accueil si l'utilisateur est connecté
    return redirect('/connexion') # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

@app.route('/accueil')
def accueil():
    """
    >>> from flask import render_template
    >>> total, salons = NSI.liste_salons()
    >>> accueil()
    <Response 200>
    """
    # Récupère la liste des salons et le total de salons
    total, salons = NSI.liste_salons()
    return render_template('accueil.html', salons=salons) # Affiche la page d'accueil avec la liste des salons

@app.route('/connexion', methods=['GET', 'POST'])
def login():
    """
    >>> from flask import request
    >>> request.method = 'POST'
    >>> request.form['pseudo'] = 'testuser'
    >>> login()
    <Response 302>
    """
    error = '' # Initialise une variable pour stocker les messages d'erreur

    if request.method == 'POST': # Vérifie si la requête est de type POST 
        pseudo = request.form['pseudo'] # Récupère le pseudo soumis par l'utilisateur
        if len(pseudo) > 3: # Vérifie que le pseudo a plus de 3 caractères
            utilisateur = NSI.nouvel_utilisateur(pseudo) # Crée un nouvel utilisateur avec le pseudo
            if utilisateur is not None: # Vérifie si l'utilisateur n'existe pas déjà
                session['user'] = utilisateur # Stocke les informations de l'utilisateur dans la session
                return redirect('/accueil') # Redirige vers la page d'accueil
            else:
                error = 'Ce pseudo est déja utilisé!' # Message d'erreur si le pseudo est déjà utilisé
        else:
            error = "Ce pseudo n'est pas valide" # Message d'erreur si le pseudo est trop court

    return render_template('connexion.html', error=error) # Affiche la page de connexion avec le message d'erreur

@app.route('/déconexion', methods=['GET'])
def logout():
    """
    >>> from flask import session
    >>> session['user'] = {'id': 1}
    >>> logout()
    <Response 302>
    """
    id = session['user']['id'] # Récupère l'ID de l'utilisateur
    NSI.supression_utilisateur(id) # Supprime l'utilisateur
    session.pop('user') # Supprime les informations de l'utilisateur de la session
    return redirect('/connexion') # Redirige vers la page de connexion

@app.route('/nouveau_salon', methods=['GET', 'POST'])
def new_room():
    """
    >>> from flask import request
    >>> request.method = 'POST'
    >>> request.form['salon'] = 'testroom'
    >>> new_room()
    <Response 302>
    """
    error = '' # Initialise une variable pour stocker les messages d'erreur

    if request.method == 'POST': # Vérifie si la requête est de type POST
        nom_salon = request.form['salon'] # Récupère le nom du salon soumis par l'utilisateur
        if len(nom_salon) > 3: # Vérifie que le nom du salon a plus de 3 caractères
            nouveau_salon = NSI.création_salon(nom_salon, session['user']) # Crée un nouveau salon
            return redirect('/accueil') # Redirige vers la page d'accueil
        else:
            error = "le nom n'est pas valide" # Message d'erreur si le nom du salon est trop court

    return render_template('nouveau_salon.html', error=error) # Affiche la page de création de salon avec le message d'erreur

@app.route('/salon/<int:id_salon>')
def discussion(id_salon):
    """
    >>> discussion(1)
    <Response 200>
    """
    return render_template("chat.html", id_salon=id_salon) # Affiche la page de chat pour le salon spécifié

@socketIO.on('message')
def handle_message(data):
    print(data) # Affiche les données reçues
    print(session) # Affiche les informations de session
    id_salon = data['id_salon'] # Récupère l'ID du salon
    message = data['message'] # Récupère le message
    id_sender = data['id_sender'] # Récupère l'ID de l'expéditeur
    data['name'] = NSI.selection_utilisateur(id_sender) # Récupère le pseudo de l'expéditeur
    print(data) # Affiche les données mises à jour
    messages_filtrees = NSI.lecture_message(id_salon) # Récupère les messages filtrés pour le salon
    print(f"{messages_filtrees['envoyeur']} : {messages_filtrees['message']}") # Affiche les messages filtrés
    emit('message', data, broadcast=True) # Envoie le message à tous les clients connectés
    NSI.nouveau_message(id_sender, id_salon, message) # Ajoute le nouveau message au salon

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html') # Gère les erreurs 404 en affichant une page d'erreur personnalisée

@app.errorhandler(500)
def cttcasé(error):
    return render_template('cassé.html') # Gère les erreurs 500 en affichant une page d'erreur personnalisée

if __name__ == '__main__':
    socketIO.run(app) # Démarre l'application Flask avec SocketIO
    
if __name__ == "__main__":
    doctest.testmod
