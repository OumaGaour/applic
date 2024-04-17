import streamlit as st
from db.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

form = st.form("register")
email = form.text_input("Enter your email")
password = form.text_input("Enter your password", type="password")
clicked_login = st.button("Already registered? Click here to login!")

# Condition pour vérifier si l'utilisateur est déjà inscrit
if clicked_login:
    switch_page("login")  # Rediriger vers la page de connexion

# Bouton pour soumettre le formulaire d'inscription
submit = form.form_submit_button("Register")
if submit:
    # Procéder à l'inscription de l'utilisateur
    result = register(email, password)
    if result == "success":
        st.success("Registration successful!")
        if st.session_state.profile == "Institute":
            switch_page("institute")
        elif st.session_state.profile == "Verifier":
            switch_page("verifier")
        elif st.session_state.profile == "Student":  # Nouvelle condition pour les étudiants
            # Rediriger vers la page de tableau de bord des étudiants après l'inscription réussie
            switch_page("student_dashboard")
    else:
        st.error("Registration unsuccessful!")
