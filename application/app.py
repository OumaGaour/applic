import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.title("Certificate Verification System")
st.write("")
st.subheader("Select Your Role")

# Utilisation d'icônes à la place des images
institute_icon = "🏢"
verifier_icon = "🔍"
student_icon = "🎓"

# Création d'une seule colonne pour toutes les options
col1 = st.columns(1)[0]  # Changez le nombre de colonnes à 1 et prenez la première colonne

# Option pour l'institut
with col1:
    clicked_institute = st.button(f"{institute_icon} Institute", key="institute")  # Ajoutez une clé unique pour chaque bouton

# Option pour le vérificateur
with col1:
    clicked_verifier = st.button(f"{verifier_icon} Verifier", key="verifier")  # Ajoutez une clé unique pour chaque bouton

# Option pour l'étudiant
with col1:
    clicked_student = st.button(f"{student_icon} Student", key="student")  # Ajoutez une clé unique pour chaque bouton

# Gestion des clics sur les boutons
if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
elif clicked_student:
    st.session_state.profile = "Student"
    switch_page('login')
