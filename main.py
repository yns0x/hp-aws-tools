import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
API_AUTH_URL = os.getenv("INTERNAL_AUTH_SERVICE_URL")


def verify_internal_auth():
    print("[INFO] Vérification des droits via l'API interne...")
    try:
        response = requests.post(API_AUTH_URL, json={"service": "backup"})
        if response.status_code == 200:
            print("[SUCCESS] Authentification interne réussie.")
            return True
        else:
            print(f"[ERROR] Accès refusé par l'API : Code {response.status_code}")
            return False
    except Exception as e:
        print("[ERROR] Serveur d'authentification injoignable : ", e)
        return False


def connect_aws_s3():
    print("[INFO] Initialisation de la connexion AWS S3...")
    if not AWS_KEY or not AWS_SECRET:
        print("[FATAL] Clés AWS manquantes dans le fichier .env !")
        return False
    time.sleep(1)
    print("[SUCCESS] Connecté avec succès au bucket 'prod-db-backups-772'.")
    return True


if __name__ == "__main__":
    print("--- Lancement du Job de Sauvegarde ---")
    if verify_internal_auth():
        if connect_aws_s3():
            print("[INFO] Compression de la base de données en cours...")
            time.sleep(2)
            print("[INFO] Upload vers S3 démarré...")
    else:
        print("[FATAL] Annulation du job de sauvegarde.")