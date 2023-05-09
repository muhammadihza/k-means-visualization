import streamlit as st
import pandas as pd  # pip install pandas
import numpy as np
import plotly.express as px  # pip install plotly-express
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title='K-Means Klastering', page_icon='📈')
st.title("Klasterisasi 📈" )


df = st.session_state["uploaded_file"].copy()


df.dropna(inplace=True)
st.subheader('Deskripsi Data')
st.write(df.describe())

scaler = StandardScaler()

st.markdown('---')
st.subheader('Mengganti Label Kolum')
df[['RHOB_T', 'GR_T', 'NPHI_T', 'PEF_T', 'DTC_T']] = scaler.fit_transform(df[['RHOB', 'GR', 'NPHI', 'PEF', 'DTC']])
df
# st.write(st.session_state["uploaded_file"].head(5))
# st.write(df['GR'])
# df = uploaded_file
# st.write(type(uploaded_file))
# df = pd.read_csv(uploaded_file)
# df = pd.read_csv(uploaded_file)
# df = pd.read_csv(uploaded_file, index_col= 'DEPTH_MD')
# st.write(df.head(3))


# --------Create function to work out optimum number of clusters---- #
st.markdown('---')
st.subheader('Fungsi optimasi jumlah klaster')
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
st.subheader('Melakukan Klaster menggunakan K-Means')
n_klaster = st.slider("Masukkan nilai untuk n klaster", 1, 10)
kmeans = KMeans(n_clusters=n_klaster)
kmeans.fit(df[['RHOB_T', 'NPHI_T']])
df['kmeans_3'] = kmeans.labels_
df


st.markdown('---')
st.subheader('Ploting Hasil')
plot_fig = plt.figure(figsize=(10,10))
plt.scatter(x=df['NPHI'], y=df['RHOB'], c=df['kmeans_3'])
plt.xlim(-0.1, 1)
plt.ylim(3, 1.5)
# plt.show()
st.pyplot(plot_fig)

if "hasil_kmeans" not in st.session_state:
    st.session_state["hasil_kmeans"] = ""

hasil_kmeans = df

proses_hasil = st.button("Lihat Grafik")
if proses_hasil:
    st.session_state["hasil_kmeans"] = hasil_kmeans
    st.success('Memproses Hasil', icon="✅")