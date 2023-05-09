import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Support', page_icon='📈')

with st.sidebar:
    selected = option_menu(
        menu_title="K-Means",
        options=["Kontak", "Tentang"]
    )