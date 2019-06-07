#!/usr/bin/python
# Import des modules nécéssaires

import os               # Manipulation des dossiers et fichiers
import time             # Date du jour
import pipes            # Compression
import configuration    # Fichier configuration.py
import subprocess       # Etape de sauvegarde



#Test qui vérifie que la variable DB_NAME existe vraiment ou pas. Si non message, si oui exécution du script.

try:
    configuration.DB_NAME
except (AttributeError, NameError):         # Si erreur système à cause de la variable non renseignée
	print("Veuillez indiquer le chemin du fichier txt ou indiquer le nom de la base à sauvegarder dans le fichier configuration")

else:
    
    
# récupération de la date actuelle pour créer un dossier de sauvegarde dans le dossier souhaité

     DATETIME = time.strftime('%Y%m%d-%H%M%S')
     TODAYBACKUPPATH = configuration.BACKUP_PATH + '/' + DATETIME

# vérification de l'existence du dossier sauvegarde, si non, création

     try:
         os.stat(TODAYBACKUPPATH)       # Vérification
     except:
         os.mkdir(TODAYBACKUPPATH)      # Création

# code pour vérifier si on souhaite faire une sauvegarde d'une seule base de données ou assigner plusieurs
# bases de données dans DB_NAME

     print ("Vérification des noms de fichiers SQL.")
     if os.path.exists(configuration.DB_NAME):          # Si le fichier txt existe alors...
         file1 = open(configuration.DB_NAME)            # Ouvrir le fichier txt
         multi = 1                                      # Indiquer qu'il y a donc plusieurs bases de données en attribuant 1 à la variable 
         print ("noms de bases de données trouvés dans le fichier txt...")
         print ("Début de la sauvegarde de toutes les bases de données listées dans le fichier " + configuration.DB_NAME)
     else:
         print ("Fichier regroupant les bases de données non trouvé...")            # Autre condition si aucun fichier txt n'est trouvé
         print ("Sauvegarde de la base de données " + configuration.DB_NAME)        # Si aucun fichier, ci-dessous se fera la sauvegarde de la base de données indiqué dans la variable DB_NAME
         multi = 0                                                                  # De plus, 0 sera attribué à la variable multi
	
# Fonction de fin du script indiquant le bon fonctionnement et la sauvegarde des bases.	

     def finsave():
         print ("")
         print ("Sauvegarde effectuée")
         print ("Les sauvegardes ont été créés dans '" + TODAYBACKUPPATH + "'")

# Fonction qui permet de séparer les bases sans et avec schéma, de trier les mauvaises bases et sauvegarder puis compresser les bonnes.

     def dumpgzip():
         dumpcmd = subprocess.Popen("mysqldump " + " -d " + " -u " + configuration.DB_USER + " -p" + configuration.DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "sansdonnees.sql", shell=True)
         dumpcmd = subprocess.Popen("mysqldump " + " -u " + configuration.DB_USER + " -p" + configuration.DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "avecdonnees.sql", shell=True)
         dumpcmd.communicate()                  # En attente d'une erreur venant du processus
         if dumpcmd.returncode != 0:            # Si dumpcmd retour un message d'erreur alors...
             print("Une erreur est survenue. Veuillez vérifier le fichier texte. Base non existante : " + db)
             mavar = db
             supp()                             # Supprimer les fichiers .sql erronés
         else:
             gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "sansdonnees.sql"        # Compression du fichier sans données
             os.system(gzipcmd)
             gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "avecdonnees.sql"        # Compression du fichier avec données
             os.system(gzipcmd)
             finsave()                                                                              # Utilisation de la fonction "finsave" pour marquer la fin du script

# Fonction permettant la suppression des bases erronnées		

     def supp():
         mavar = db
         os.remove(TODAYBACKUPPATH + "/" + mavar + "sansdonnees.sql")
         os.remove(TODAYBACKUPPATH + "/" + mavar + "avecdonnees.sql")
         print ("Suppression de la sauvegarde " + mavar + " ...Fait.")
  



# Dans le cas ou le fichier txt est utilisé pour plusieurs bases de données

     if multi:
         in_file = open(configuration.DB_NAME,"r")      # Si multi = 1 alors ouvrir le fichier txt et le lire grâce à l'option r de la fonction open disponible par défaut en python
         flength = len(in_file.readlines())             # Lecture du nombre de lignes présentes dans le fichier txt
         in_file.close()                                # fermeture du fichier
         p = 1                                          # attribution de 1 à la variable p
         dbfile = open(configuration.DB_NAME,"r")       # Puis ouverture du ficher txt et lecture de ce fichier
         while p <= flength:                            # Tant que p qui est égale à 1 est inférieure ou égale à flength = au nombre de lignes du fichier txt (donc si au moins une ligne dans le fichier txt) alors..
             db = dbfile.readline() # Lecture du nom des bases de données dans le fichier
             db = db[:-1]           # Suppression du retour à la ligne "retour chariot" puisqu'on n'a plus de bases de données à sauvegarder
             mavar = db
             dumpgzip()             # Utilisation de la fonction dumpzip
             p = p + 1
         dbfile.close()             # Fermeture du fichier txt

# Dans le cas où le nom d'une seule base de donnée a été assignée à la variable DB_NAME

     else:
         db = configuration.DB_NAME
         mavar = (configuration.DB_NAME)
         dumpgzip()                                         # Sauvegarde puis compression
         finsave()                                          # fin du script
         if not os.listdir(TODAYBACKUPPATH):                # Dans le cas où le dossier est vide, le supprimer
                 os.rmdir(TODAYBACKUPPATH)
                 print ("Annulation de la sauvegarde. Veuillez vérifier le fichier de configuration.")
		
