import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import os
from streamlit_option_menu import option_menu
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from db.firebase_app import save_student_info, save_certificate_request
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

# Définir les options du menu
options = ["Informations", "Demande de certificat ", "View certificat" ,"logout"]

# Personnaliser l'apparence du menu
selected = option_menu(
    menu_title=None,
    options=options,
    icons=[ "person", "envelope", "eye", "box-arrow-in-right"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Informations":
    st.title("Formulaire d'informations ")
    identifiant = st.text_input("Identifiant de l'étudiant")
    nom = st.text_input("Nom de l'étudiant")
    prenom = st.text_input("Prénom de l'étudiant")
    email = st.text_input("email de l'étudiant")
    notes = st.text_input("notes de l'étudiant")
    filiere_options = ['IGE', 'SMI', 'SMP', 'MASD', 'GPCA', 'LEA']
    filiere = st.selectbox("filiere de l'étudiant", filiere_options)
    telephon = st.text_input("Telephone de l'étudiant")
    birthday = st.text_input("birthday de l'étudiant")
    position = st.text_input("position de l'étudiant")
    


    # Bouton pour soumettre le formulaire
    if st.button("Enregestrer"):
        # Créez un dictionnaire avec les données de l'étudiant
        if save_student_info(identifiant,nom, prenom, email,  notes, filiere, telephon,  birthday, position):
            st.write("Données enregistrées avec succès !")
        else:
            st.write("Une erreur s'est produite lors de l'enregistrement des données.")
        

elif selected == "Demande de certificat ":
    st.title(f"{selected}")
    #demander les certificat et(pour apres)  tous les document universitaireas (utilisation dun fichier qui contien les document csv)
    identifiant = st.text_input("identifiant")
    nom = st.text_input("Nom de l'étudiant")
    prenom = st.text_input("Prénom de l'étudiant")
    filiere = st.text_input("filiere de l'étudiant")
    notes = st.text_input("notes de l'étudiant")
    birthday = st.text_input("birthday de l'étudiant")
     
    if st.button("demander"):
        if save_certificate_request(identifiant, nom, prenom, filiere, notes, birthday):
            st.write("Demande envoyée avec succès !")
        else:
            st.write("Une erreur s'est produite lors de l'enregistrement de la demande de certificat.")
elif selected == "logout":
   switch_page('app')