import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Home', page_icon='📈')

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Data"]
    )

if selected == "Data":

    st.title('Excel Plotter 📈')
    st.subheader('Silahkan msukkan dataset')



    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = ""

    uploaded_file = st.file_uploader('Choose a XLSX file', type='csv')
    # st.write(type(uploaded_file))

    if uploaded_file:
        st.markdown('---')
        # df = pd.read_csv(uploaded_file, index_col= 'DEPTH_MD')
        df = pd.read_csv(uploaded_file)

        df
        # df = pd.read_excel(uploaded_file, engine='openpyxl')
        # st.dataframe(df)
        

        proses = st.button("Proses")
        if proses:
            st.session_state["uploaded_file"] = df
            # st.session_state["uploaded_file"] = uploaded_file
            # st.balloons()
            st.success('Berhasil Memasukkan File!', icon="✅")


        # st.session_state["stateA"] = "A"
        # varA = st.session_state["stateA"]
        # st.session_state["stateB"] = "B"
        # st.session_state["stateC"] = st.session_state["stateB"]

        # st.write(varA, st.session_state["stateC"])