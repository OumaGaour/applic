import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID", "logout")
# Personnaliser l'apparence du menu
selected = option_menu(
    menu_title=None,
    options=options,
    icons=["patch-check", "eye", "box-arrow-in-right"],
    default_index=0,
    orientation="horizontal",
)

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            (uid, candidate_name, course_name, notes, grad, org_name, birthday) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            data_to_hash = f"{uid}{candidate_name}{course_name}{notes}{grad}{org_name}{birthday}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificated verified successfully!")
            else:
                st.error("Invalid Certificate! Certificate might be tampered")
        except Exception as e:
            st.error("Error Invalid Certificate! ")


elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Validate")
    if submit:
        try:
            view_certificate(certificate_id)
            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificated verified successfully!")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")
elif selected == "logout":
   switch_page('app')
