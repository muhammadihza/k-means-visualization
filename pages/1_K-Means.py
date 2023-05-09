import streamlit as st
import pandas as pd  # pip install pandas
import numpy as np
import plotly.express as px  # pip install plotly-express
import matplotlib.pyplot as plt
import base64  # Standard Python Module

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from streamlit_option_menu import option_menu
from io import StringIO, BytesIO  # Standard Python Module

st.set_page_config(page_title='K-Means Klastering', page_icon='📈')

with st.sidebar:
    selected = option_menu(
        menu_title="K-Means",
        options=["Klasterisasi", "Grafik", "Dashboard"]
    )

df = st.session_state["uploaded_file"].copy()

if selected == "Klasterisasi":

    st.title("Klasterisasi 📈" )
    
    df.dropna(inplace=True)
    st.subheader('Deskripsi Data')
    st.write(df.describe())

    scaler = StandardScaler()

    st.markdown('---')
    st.subheader('Mengganti Label Kolum')
    df[['RHOB_T', 'GR_T', 'NPHI_T', 'PEF_T', 'DTC_T']] = scaler.fit_transform(df[['RHOB', 'GR', 'NPHI', 'PEF', 'DTC']])
    df

    if "df_label_updated" not in st.session_state:
        st.session_state["df_label_updated"] = ""

    st.session_state["df_label_updated"] = df

    st.markdown('---')
    st.subheader('Melakukan Klaster menggunakan K-Means')
    n_klaster = st.slider("Tentukan nilai untuk n klaster", 1, 10)
    kmeans = KMeans(n_clusters=n_klaster)
    kmeans.fit(df[['RHOB_T', 'NPHI_T']])
    df['kmeans_3'] = kmeans.labels_
    df

    if "df_label_second_updated" not in st.session_state:
        st.session_state["df_label_second_updated"] = ""

    st.session_state["df_label_second_updated"] = df


    


elif selected == "Grafik":
    # --------Create function to work out optimum number of clusters---- #
    st.title("Grafik Hasil 📈" )
    st.subheader('Fungsi optimasi jumlah klaster')

    df = st.session_state["df_label_updated"]


    optimasi_klaster = st.slider("Tentukan jumlah klaster", 2, 10)
    st.write("Jumlah klaster adalah", optimasi_klaster)
    def optimise_k_means(data, max_k):
        means = []
        inertias = []

        for k in range(1, max_k):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data)

            means.append(k)
            inertias.append(kmeans.inertia_)

        #Generate the elbow plot
        fig = plt.figure(figsize=(10,5))
        plt.plot(means, inertias, 'o-')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.grid(True)
        st.pyplot(fig)

    optimise_k_means(df[['RHOB_T', 'GR_T']], optimasi_klaster)


    st.markdown('---')
    st.subheader('Ploting Hasil')

    # inisialisasasi perubahan dataframe
    df = st.session_state["df_label_second_updated"]

    # menampilkan figure
    plot_fig = plt.figure(figsize=(10,10))
    plt.scatter(x=df['NPHI'], y=df['RHOB'], c=df['kmeans_3'])
    plt.xlim(-0.1, 1)
    plt.ylim(3, 1.5)
    # plt.show()
    st.pyplot(plot_fig)

    # membuat tombol untuk menampilkan grafik
    if "hasil_kmeans" not in st.session_state:
        st.session_state["hasil_kmeans"] = ""

    hasil_kmeans = df

    proses_hasil = st.button("Lihat Grafik")
    if proses_hasil:
        st.session_state["hasil_kmeans"] = hasil_kmeans
        st.success('Memproses Hasil', icon="✅")



elif selected == "Dashboard":

    def generate_excel_download_link(df_grouped):
        # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
        towrite = BytesIO()
        df_grouped.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
        return st.markdown(href, unsafe_allow_html=True)

    def generate_html_download_link(fig):
        # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
        towrite = StringIO()
        fig.write_html(towrite, include_plotlyjs="cdn")
        towrite = BytesIO(towrite.getvalue().encode())
        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
        return st.markdown(href, unsafe_allow_html=True)


    st.header('Hasil Klasterisasi')

    ### --- LOAD DATAFRAME
    df = st.session_state['hasil_kmeans'].copy()

    st.markdown('---')
    genre = st.radio(
        "Pilih atribut",
        ['RHOB', 'GR', 'NPHI', 'PEF', 'DTC'],
        horizontal= True,
        # label_visibility= 'visible',
        # disabled=True
        )


    if genre == 'RHOB':
        value = 'RHOB'
    elif genre == 'GR':
        value = 'GR'
    elif genre == 'NPHI':
        value = 'NPHI'
    elif genre == 'PEF':
        value = 'PEF'
    elif genre == 'DTC':
        value = 'DTC'
        

    pie_chart = px.pie(df,
                    title='Grafik hasil kelompok berdasarkan atribut',
                    values=value,
                    names='kmeans_3')

    st.plotly_chart(pie_chart)

    st.markdown('---')
    

    klaster = st.sidebar.multiselect(
        "Pilih Klaster:",
        options=df["kmeans_3"].unique(),
        default=df["kmeans_3"].unique()
    )

    df_selection = df.query(
        "kmeans_3 == @klaster"
    )

    st.dataframe(df_selection)













    fig = pie_chart
    df_grouped = df.copy()
#---------------------------------------------------------------------#
    # kelompok = df['kmeans_3'].unique().tolist()

    # pilihan_kelompok = st.multiselect('kelompok:',
    #                                   kelompok,
    #                                   default=kelompok)

    # mask = (df['RHOB']) & (df['kelompok'].isin(pilihan_kelompok))
    # jumlah_hasil = df[mask].shape[0]
    # st.markdown(f'*Hasil yang didapati: {jumlah_hasil}*')
#---------------------------------------------------------------------#

    # -- DOWNLOAD SECTION
    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)