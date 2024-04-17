import pyrebase
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

db = firebase.database()


def register(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "failure"


def login(email, password):
    try:
        auth.sign_in_with_email_and_password(email, password)
        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "failure"



def login_student(email, password):
    try:
        auth.sign_in_with_email_and_password(email, password)
        return "success"
    except Exception as e:
        print(f"Error: {e}")
        return "failure"

def save_student_info(identifiant,nom, prenom, email,  notes, filiere, telephon,  birthday, position):
    try:
        # Enregistrer les données dans Firebase
        db.child("etudiants").child(identifiant).set({
            "identifiant": identifiant,
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "notes": notes,
            "filiere": filiere,
            "telephon": telephon,  
            "birthday": birthday,
            "position": position
        })
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des informations de l'étudiant : {e}")
        return False


def save_certificate_request(identifiant, nom, prenom, filiere, notes, birthday):
    try:
        # Enregistrer les données dans Firebase
        db.child("certificats").child(identifiant).set({
            "identifiant": identifiant,
            "nom": nom,
            "prenom": prenom,
            "filiere": filiere,
            "notes": notes,
            "birthday": birthday

        })
        return True
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la demande de certificat : {e}")
        return False

def get_certificate_requests():
  """Récupère les demandes de certificats depuis Firebase et les retourne dans un tableau."""
  requests = []
  for request in db.child("certificats").get().each():
    requests.append([request.val()['identifiant'], request.val()['nom'], request.val()['prenom'], request.val()['filiere'], request.val()['notes'], request.val()['birthday']])
  return requests


def update_request_status(request_id, new_status):
    try:
        # Mise à jour du statut de la demande dans Firebase
        db.child("certificats").child(request_id).update({"statut": new_status})
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du statut de la demande : {e}")
        return False





  