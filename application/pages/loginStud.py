import streamlit as st
from db.firebase_app import login_student
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

form = st.form("login")
email = form.text_input("Enter your email")
password = form.text_input("Enter your password", type="password")

# Condition pour vérifier si l'utilisateur est un nouvel utilisateur
if st.session_state.profile != "Institute" and st.session_state.profile != "Verifier":
    # Bouton pour rediriger vers la page d'inscription
    clicked_register = st.button("New user? Click here to register!")

    if clicked_register:
        switch_page("registerStud")

# Bouton pour soumettre le formulaire de connexion
submit = form.form_submit_button("Login")
if submit:
    # Vérifier le type d'utilisateur et procéder à l'authentification
    if st.session_state.profile == "Student":  
        result = login_student(email, password)  # Modifier la fonction de connexion pour les étudiants
        if result == "success":
            st.success("Login successful!")
            st.session_state.email = email  # Initialiser st.session_state.email avec l'e-mail de l'utilisateur
            switch_page("student_dashboard")  # Rediriger vers le tableau de bord des étudiants après la connexion réussie
        else:
            st.error("Invalid credentials!") 
