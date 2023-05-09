import pandas as pd
import streamlit as st
import plotly.express as px
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module

st.set_page_config(page_title='Hasil Klasterisasi', page_icon='📉')

def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
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
st.subheader('Apakah ini membantu?')

### --- LOAD DATAFRAME
df = st.session_state['hasil_kmeans'].copy()
df

df_grouped = df.copy()


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
                   title='Grafik hasil kelompok untuk atribut',
                   values=value,
                   names='kmeans_3')

st.plotly_chart(pie_chart)
fig = pie_chart

# kelompok = df['kmeans_3'].unique().tolist()

# pilihan_kelompok = st.multiselect('kelompok:',
#                                   kelompok,
#                                   default=kelompok)

# mask = (df['RHOB']) & (df['kelompok'].isin(pilihan_kelompok))
# jumlah_hasil = df[mask].shape[0]
# st.markdown(f'*Hasil yang didapati: {jumlah_hasil}*')

# -- DOWNLOAD SECTION
st.subheader('Downloads:')
generate_excel_download_link(df_grouped)
generate_html_download_link(fig)