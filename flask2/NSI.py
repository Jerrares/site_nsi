import pandas as pd
import secrets as sc





def liste_salons():

    try:
        salons = pd.read_csv('.data/salons.csv') #on essaie de lire le fichier qui contient la liste des salons

    except:
        return 0,[]# si l'essai est un echec alors on renvoie un tableau vide car aucun salon n'a été créé

    total = len(salons)# cette partie compte le nombre de salons
    salons = salons.to_dict(orient='records')#converti la variable salon en une liste de dictionaire 


    return total, salons#on renvoie le nombre total de salons et la liste de dictionnaire 







def nouvel_utilisateur(pseudo):

    try:
        utilisateurs = pd.read_csv('.data/utilisateurs.csv')#on essaie de lire le fichier utilisateurs.csv et de stocker son contenu dans la variable utilisateurs 

    except:
        utilisateurs = pd.DataFrame(columns=['id', 'pseudo'])#si on ne réussit pas a le lire on en déduit qu'il n'éxiste pas donc on crée un DataFrame avec les 2 colones mais vides qui deviendra notre csv


    if not utilisateurs.empty and pseudo in utilisateurs['pseudo'].values: #on vérifie ici que utilisateurs n'est pas vide ou qu'il n'existe pas déja
        return False #si c'est le cas on renvoie False pour pouvoir passer dans le else de notre code principal

    new_id = sc.token_hex(8) #attribue simplement un code de 8 caractères aléatoires a la variable new_id

    utilisateur = {          #création d'un dictionnaire appelé utilisateur (sans s c'est important car on ne s'occupe que d'un donc attention utilisateur != utilisateurs)
        'id': new_id,        #on crée ici la colone de l'identifiant (id) qui contient l'id de l'utilisateur
        'pseudo': pseudo     #on crée ici la colone du pseudo qui lui est attribué
    }

    utilisateurs = pd.concat([utilisateurs, pd.DataFrame(utilisateur,index=[0])], ignore_index=True) #ici on met a jour le dataframe qui contient la liste des utilisateurs en y ajoutant le nouveau
    utilisateurs.to_csv('.data/utilisateurs.csv', index=False)#ici on met a jour utilisaturs.csv (la liste des utilisateurs) en transformant le dataframe utilisateurs en un csv 
    return utilisateur #on renvoie la valleur de user qui va servir dans le code principal














def supression_utilisateur(id):

    utilisateurs = pd.read_csv('.data/utilisateurs.csv')#on lit le fichier utilisateurs.csv et on stocke son contenu dans la variable utilisateurs

    if not utilisateurs.empty and id in utilisateurs['id'].values:#on vérifie ici que utilisateurs et que l'id récupéré est valide
        utilisateurs = utilisateurs.drop(utilisateurs[utilisateurs['id'] == id].index)#ici on suprime l'utilisateur qui a le meme id que celui qui nous a été fourni ( on suprime un index donc on récupère son index)
        utilisateurs.to_csv('.data/utilisateurs.csv', index=False)#ici on met a jour utilisaturs.csv (la liste des utilisateurs) en transformant le dataframe utilisateurs en un csv
        
        
        

















def création_salon(nom_salon, utilisateur):
    try:
        salons = pd.read_csv('.data/salons.csv')#on essaie de lire le fichier salons.csv et de stocker son contenu dans la variable salons

    except:
        salons = pd.DataFrame(columns=['id', 'nom', 'créateur', 'cible', 'messages'])#si on ne réussit pas a le lire on en déduit qu'il n'éxiste pas donc on crée un DataFrame avec les 5 colones mais vides qui deviendra notre csv

    new_id = sc.token_hex(8) #attribue simplement un code de 8 caractères aléatoires a la variable new_id

    nouveau_salon = {             #création d'un dictionnaire appelé nouveau_salon
        'id': new_id,             #on crée ici la colone de l'identifiant (id) qui contient l'id du salon
        'nom': nom_salon,         #on crée ici la colone du nom du salon
        'créateur': utilisateur['id'],   #on crée ici la colone de l'identifiant (id) qui contient l'id de l'utilisateur qui a créé le salon
        'cible': 15,              #on crée ici la colone du nombre de personnes censé pouvoir rejoindre le salon (a vérifier) 
        'messages': ''            #on crée ici la colone qui contient les messages du salon
    }

    salons = pd.concat([salons, pd.DataFrame(nouveau_salon, index=[0])], ignore_index=True)#ici on met a jour le dataframe qui contient la liste des salons en y ajoutant le nouveau
    salons.to_csv('.data/salons.csv', index=False)#ici on met a jour salons.csv (la liste des salons) en transformant le dataframe salons en un csv

    return nouveau_salon#on renvoie la valleur de nouveau_salon qui va servir dans le code principal