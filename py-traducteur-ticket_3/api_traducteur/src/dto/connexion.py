import mysql.connector as mysqlpyth

from config.parametres import BDD_USER, BDD_PASSWORD, BDD_HOST, BDD_PORT, BDD_DATABASE

class Connexion :

    @classmethod
    def ouvrir_connexion(cls):
        cls.bdd = mysqlpyth.connect(user=BDD_USER, password=BDD_PASSWORD, host=BDD_HOST, port=BDD_PORT, database=BDD_DATABASE)
        cls.cursor = cls.bdd.cursor(dictionary=True)

    @classmethod
    def fermer_connexion(cls):
        cls.cursor.close()
        cls.bdd.close()