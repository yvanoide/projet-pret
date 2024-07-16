# Utilisez l'image de base MySQL
FROM mysql

# Définir les variables d'environnement pour MySQL
ENV MYSQL_ROOT_PASSWORD=example
ENV MYSQL_DATABASE=traducteur
ENV MYSQL_USER=traducteur
ENV MYSQL_PASSWORD=traducteur

# Copier le script SQL d'initialisation dans le répertoire d'initialisation de MySQL
COPY init.sql /docker-entrypoint-initdb.d/

# Définir le point d'entrée par défaut pour lancer MySQL
CMD ["mysqld"]
