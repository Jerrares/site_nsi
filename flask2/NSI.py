import pandas as pd
import doctest
# Fonction pour lister tous les salons disponibles
def liste_salons():
    try:
        salons = pd.read_csv('.data/salons.csv') # Tentative de lecture du fichier CSV contenant la liste des salons
    except:
        return 0, [] # En cas d'échec, retourne un tableau vide car aucun salon n'a été créé

    total = len(salons) # Compte le nombre total de salons
    salons = salons.to_dict(orient='records') # Convertit le DataFrame en une liste de dictionnaires pour une meilleure manipulation

    return total, salons # Retourne le nombre total de salons et la liste des salons

# Fonction pour créer un nouvel utilisateur
def nouvel_utilisateur(pseudo):
    try:
        utilisateurs = pd.read_csv('.data/utilisateurs.csv') # Tentative de lecture du fichier CSV contenant la liste des utilisateurs
    except:
        utilisateurs = pd.DataFrame(columns=['id', 'pseudo']) # Si le fichier n'existe pas, crée un nouveau DataFrame avec les colonnes nécessaires

    if not utilisateurs.empty and pseudo in utilisateurs['pseudo'].values: # Vérifie si le pseudo existe déjà
        return None # Si le pseudo existe déjà, retourne None

    new_id = len(utilisateurs) + 1 # Attribue un nouvel ID à l'utilisateur

    utilisateur = { # Crée un dictionnaire pour l'utilisateur
        'id': new_id, # ID de l'utilisateur
        'pseudo': pseudo # Pseudo de l'utilisateur
    }

    utilisateurs = pd.concat([utilisateurs, pd.DataFrame(utilisateur, index=[0])], ignore_index=True) # Ajoute le nouvel utilisateur au DataFrame
    utilisateurs.to_csv('.data/utilisateurs.csv', index=False) # Sauvegarde le DataFrame mis à jour dans le fichier CSV

    return utilisateur # Retourne le dictionnaire de l'utilisateur

# Fonction pour supprimer un utilisateur
def supression_utilisateur(id):
    """
    >>> supression_utilisateur(1)
    """
    utilisateurs = pd.read_csv('.data/utilisateurs.csv') # Lit le fichier CSV contenant la liste des utilisateurs

    if not utilisateurs.empty and id in utilisateurs['id'].values: # Vérifie si l'ID existe dans la liste des utilisateurs
        utilisateurs = utilisateurs.drop(utilisateurs[utilisateurs['id'] == id].index) # Supprime l'utilisateur de la liste
        utilisateurs.to_csv('.data/utilisateurs.csv', index=False) # Sauvegarde la liste mise à jour dans le fichier CSV

# Fonction pour créer un nouveau salon
def création_salon(nom_salon, utilisateur):
    try:
        salons = pd.read_csv('.data/salons.csv') # Tentative de lecture du fichier CSV contenant la liste des salons
    except:
        salons = pd.DataFrame(columns=['id', 'nom', 'créateur', 'cible']) # Si le fichier n'existe pas, crée un nouveau DataFrame avec les colonnes nécessaires

    new_id = len(salons['id']) + 1 # Attribue un nouvel ID au salon

    nouveau_salon = { # Crée un dictionnaire pour le nouveau salon
        'id': new_id, # ID du salon
        'nom': nom_salon, # Nom du salon
        'créateur': utilisateur['id'], # ID de l'utilisateur qui crée le salon
        'cible': 0 # Nombre de personnes censées pouvoir rejoindre le salon (à vérifier)
    }

    salons = pd.concat([salons, pd.DataFrame(nouveau_salon, index=[0])], ignore_index=True) # Ajoute le nouveau salon au DataFrame
    salons.to_csv('.data/salons.csv', index=False) # Sauvegarde le DataFrame mis à jour dans le fichier CSV

    return nouveau_salon # Retourne le dictionnaire du nouveau salon

# Fonction pour ajouter un nouveau message à un salon
def nouveau_message(id_user, id_salon, message):

    try:
        messages = pd.read_csv('.data/messages.csv') # Tentative de lecture du fichier CSV contenant la liste des messages
    except:
        messages = pd.DataFrame(columns=['id_message', 'message', 'envoyeur', 'id_salon']) # Si le fichier n'existe pas, crée un nouveau DataFrame avec les colonnes nécessaires

    id_message = len(messages['id_message']) + 1 # Attribue un nouvel ID au message

    nouveau_message = { # Crée un dictionnaire pour le nouveau message
        'id_message': id_message, # ID du message
        'message': message, # Texte du message
        'envoyeur': id_user, # ID de l'utilisateur qui envoie le message
        'id_salon': id_salon # ID du salon dans lequel le message est envoyé
    }

    messages = pd.concat([messages, pd.DataFrame(nouveau_message, index=[0])], ignore_index=True) # Ajoute le nouveau message au DataFrame
    messages.to_csv('.data/messages.csv', index=False) # Sauvegarde le DataFrame mis à jour dans le fichier CSV

    return nouveau_message # Retourne le dictionnaire du nouveau message

# Fonction pour lire les messages d'un salon spécifique
def lecture_message(id_salon):
    try:
        messages = pd.read_csv('.data/messages.csv') # Tentative de lecture du fichier CSV contenant la liste des messages
    except:
        messages = pd.DataFrame(columns=['id_message', 'message', 'envoyeur', 'id_salon']) # Si le fichier n'existe pas, crée un nouveau DataFrame avec les colonnes nécessaires

    messages_triees = messages.sort_values(by='id_message', ascending=True) # Trie les messages par ID de message
    messages_filtrees = messages_triees[messages_triees['id_salon'] == id_salon] # Filtre les messages pour ne garder que ceux du salon spécifié
    messages_filtrees = messages_filtrees[['message', 'envoyeur']] # Sélectionne uniquement les colonnes 'message' et 'envoyeur'

    return messages_filtrees # Retourne les messages filtrés

# Fonction pour sélectionner un utilisateur par son ID
def selection_utilisateur(id):

    utilisateurs = pd.read_csv('.data/utilisateurs.csv') # Lit le fichier CSV contenant la liste des utilisateurs
    ligne_id = utilisateurs.loc[utilisateurs['id'] == int(id)] # Filtre les utilisateurs pour ne garder que celui avec l'ID spécifié
    pseudo = ligne_id.iloc[0, 1] # Récupère le pseudo de l'utilisateur
    return pseudo # Retourne le pseudo de l'utilisateur


# la plupart des fonctions on un résultat dépendant d'élément exterieur ou variables, ils ne peuvent donc etre test avec doctest


