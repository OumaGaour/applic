import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from streamlit_option_menu import option_menu
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page
from db.firebase_app import get_certificate_requests, update_request_status

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")


def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None


options = ("Generate Certificate", "View Certificates", "manage" ,"logout")
# Personnaliser l'apparence du menu
selected = option_menu(
    menu_title=None,
    options=options,
    icons=["building-lock", "eye", "gear", "box-arrow-in-right"],
    default_index=0,
    orientation="horizontal",
)


if selected == options[0]:
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="Identifiant")
    candidate_name = form.text_input(label="Nom")
    course_name = form.text_input(label="Filiere")
    notes = form.text_input(label="Note")
    grad = form.text_input(label="Grad")
    org_name = form.text_input(label="Universite")
    birthday = form.text_input(label="Annee")

    submit = form.form_submit_button("Valide")
    if submit:
        pdf_file_path = "certificate.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate(pdf_file_path, uid, candidate_name, course_name, notes, grad, org_name, birthday, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        data_to_hash = f"{uid}{candidate_name}{course_name}{notes}{grad}{org_name}{birthday}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        # Smart Contract Call
        contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, notes, grad, org_name, birthday, ipfs_hash).transact({'from': w3.eth.accounts[0]})
        st.success(f"Certificate successfully generated with Certificate ID: {certificate_id}")

elif selected == "View Certificates":
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
elif selected == "manage":
    st.title("Gestion des demandes de certificats")
    requests = get_certificate_requests()
    headers = ["Identifiant", "Nom", "Prénom", "Filière", "Notes", "Date de naissance", "Statut"]

    # Afficher la table avec les demandes et leur statut
    table_data = []
    for request in requests:
        request_id = request[0]
        row = request + [""]
        statut = st.selectbox(f"Statut de la demande {request_id}", ["En attente", "Acceptée", "Refusée"])
        if statut != request[-1]:  # Vérifier si le statut a changé
            if update_request_status(request_id, statut):
                st.write(f"Statut de la demande {request_id} mis à jour avec succès !")
            else:
                st.write(f"Échec de la mise à jour du statut de la demande {request_id}.")
        row[-1] = statut
        table_data.append(row)

    st.table([headers] + table_data)

    
elif selected == "logout":
   switch_page('app')
        
