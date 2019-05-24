# BDD SAUVE


Introduction :
 
Ce script permet la sauvegarde d'une ou plusieurs bases de données en local ou sur un disque partagé.
 
Conditions de tests :
 
Ce script a été établi dans le cadre d'un projet qui consistait à automatiser une tâche d'administration.
Ont donc été mis en place un serveur NFS partageant donc un disque ainsi qu'un serveur SQL.
Sur ce deuxième serveur a été créé le script permettant donc le backup de la base de données.
 
Résultat :
 
En condition réelle, le DBA et le responsable métier seront les principaux concernés par cette sauvegarde.
Pour cette raison, il y aura donc deux sauvegardes dont une avec les données pour le responsable métier
et une sauvegarde sans données pour le DBA considérant qu'il n'a le droit de visibilité que sur le schéma.
Ces deux sauvegardes seront compressées dans deux dossiers différents.
Les dossiers principaux seront créés et nommés avec la date du jour, minutes et secondes de la création.
 
Autres options :
 
Ce script permet de créer la sauvegarde d'une ou plusieurs bases de données.
Dans ce dernier cas, il sera nécessaire de créer un fichier .txt et d'inclure le nom des bases.
 
Prérequis :
 
- un serveur nfs
- un serveur sql ainsi que des comptes admins
- mysqldump
- le script
 
Ne pas oublier de remplacer les informations suivantes :
 
DB_USER : nom de l'utilisateur

DB_USER_PASSWORD : mot de passe de l'utilisateur

DB_NAME : nom de la base de données ou lien du fichier txt

BACKUP_PATH : lien du dossier où seront stockées les sauvegardes
 
 
Détail des options du Mysqldump :
 
"mysqldump " + " -d " + " -u " + configuration.DB_USER + " -p" + configuration.DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + "sansdonnees.sql"
 
-d : cette option permet la suppression des données dans le fichier, seul le schéma sera visible
-u : utilisateur
-p : mot de passe
