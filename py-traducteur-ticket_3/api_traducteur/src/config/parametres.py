import os

# paramètres pour le traducteur
VERSIONS = ["fr >> en","en >> fr"]

BDD_HOST = os.getenv('DATABASE_HOST', 'localhost')
BDD_PORT = os.getenv('DATABASE_PORT', 3307)
BDD_USER = os.getenv('DATABASE_USER', 'traducteur')
BDD_PASSWORD = os.getenv('DATABASE_PASSWORD', 'traducteur')
BDD_DATABASE = os.getenv('DATABASE_NAME', 'traducteur')
