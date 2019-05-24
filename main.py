#!/usr/bin/python


# Import des librairies nécessaires
 
import os
import time
import datetime
import pipes
import configuration


# récupération de la date actuelle pour créer un dossier de sauvegarde

DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = configuration.BACKUP_PATH + '/' + DATETIME

# vérification de l'existence du dossier sauvegarde, si non, création

try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)
 
# code pour vérifier si on souhaite faire une sauvegarde d'une seule base de données ou assigner plusieurs bases de données dans DB_NAME

print ("Vérification des noms de fichiers SQL.")
if os.path.exists(configuration.DB_NAME):
    file1 = open(configuration.DB_NAME)
    multi = 1
    print ("noms de bases de données trouvés dans le fichier txt...")
    print ("Début de la sauvegarde de toutes les bases de données listées dans le fichier " + configuration.DB_NAME)
else:
    print ("Fichier regroupant les bases de données non trouvé...")
    print ("Sauvegarde de la base de données " + configuration.DB_NAME)
    multi = 0
 
# Sauvegarde de la base de données

if multi:
   in_file = open(configuration.DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(configuration.DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # Lecture du nom des bases de données dans le fichier 
       db = db[:-1]         
       dumpcmd = "mysqldump " + " -d " + " -u " + configuration.DB_USER + " -p" + configuration.DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(dumpcmd)
       gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(gzipcmd)
       p = p + 1
   dbfile.close()
else:
   db = configuration.DB_NAME
   dumpcmd = "mysqldump " + " -d " + " -u " + configuration.DB_USER + " -p" + configuration.DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "sansdonnees.sql"
   os.system(dumpcmd)
   dumpcmd = "mysqldump " + " -u " + configuration.DB_USER + " -p" + configuration.DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "avecdonnees.sql"
   os.system(dumpcmd)
   gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "sansdonnees.sql"
   os.system(gzipcmd)
   gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "avecdonnees.sql"
   os.system(gzipcmd)
 
print ("")
print ("Sauvegarde effectuée")
print ("Les sauvegardes ont été créés dans '" + TODAYBACKUPPATH + "'")
