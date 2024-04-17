import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

form = st.form("login")
email = form.text_input("Enter your email")
password = form.text_input("Enter your password", type="password")

# Condition pour vérifier si l'utilisateur est un nouvel utilisateur
if st.session_state.profile != "Institute" and st.session_state.profile != "Verifier":
    # Bouton pour rediriger vers la page d'inscription
    clicked_register = st.button("New user? Click here to register!")

    if clicked_register:
        switch_page("register")

# Bouton pour soumettre le formulaire de connexion
submit = form.form_submit_button("Login")
if submit:
    # Vérifier le type d'utilisateur et procéder à l'authentification
    if st.session_state.profile == "Institute":
        valid_email = os.getenv("institute_email")
        valid_pass = os.getenv("institute_password")
        if email == valid_email and password == valid_pass:
            switch_page("institute")
        else:
            st.error("Invalid credentials!")
    elif st.session_state.profile == "Verifier":
        result = login(email, password)
        if result == "success":
            st.success("Login successful!")
            switch_page("verifier")
        else:
            st.error("Invalid credentials!")
    elif st.session_state.profile == "Student":  
        result = login(email, password)
        if result == "success":
            st.success("Login successful!")
            st.session_state.email = email  # Initialize email in session state
            switch_page("student_dashboard") 
        else:
            st.error("Invalid credentials!") 
