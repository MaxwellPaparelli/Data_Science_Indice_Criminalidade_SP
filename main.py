#Linguagem Python
#IDE PyCharm
#importaçãode biliotecas
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

#importação dos daos
data_csv = 'criminalidade_sp_2.csv'

#Armazenando os dados carregados em um cache
@st.cache

#tratamento do data frame
def load_data():

    columns = {
        'bairro': 'bairro',
        'created_at': 'data_hora',
        'descricao': 'descricao_crime',
        'endereco': 'endereco',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'registou_bo': 'registrou_bo',
    }
    data = pd.read_csv(data_csv, index_col='id')
    data = data.rename(columns=columns)
    data.data_hora = pd.to_datetime(data.data_hora)
    data = data[list(columns.values())]
    return data

#carregamento do data frame depois de tratado
df = load_data()

#Descrição inserida no Main
st.title("Criminalidade em São Paulo")
st.markdown(
    """
            A **criminalidade** é um problema recorrente no Brasil. Buscamos sempre formas de diminuir
            esses indices e usando técnicas de Ciência de Dados para conseguirmos entender melhor o que
            está acontecendo e gerar insights que direcionem ações capazes de diminuir os índices de
            criminalidade
            
            Abaixo você verá através de um mapa em quais regiões estão as maiores incidências de crimes 
            em São Paulo.
    """
    )

#slider no sidebar para filtrar o ano que irá interagir com o mapa
st.sidebar.markdown("**Slider para filtrar o ano que irá interagir com o Mapa!**")
ano_selecionado = st.sidebar.slider("Selecione um ano", 2013, 2018, 2018)
df_selected = df[df.data_hora.dt.year == ano_selecionado]

#informativo no sidebar que irá mostrar quantas linha de dados foram carregados de acordo com o filtro do slider
st.sidebar.info("Foram carregadas {} linhas".format(df_selected.shape[0]))

#Caso o usuário selecionar o checkbox irá aparecer a base de dados no main para o usuário
if st.sidebar.checkbox("Selecione para ver a base de dados!"):
    st.header("Base de dados!")
    st.write(df_selected)

#mapa que irá váriar de acordo com o filtro
st.map(df_selected)
st.markdown("")

#Gráfico de crimes por ano
st.markdown("**Gráfico de crimes registrados por ano:**")
chart1 = alt.Chart(df).mark_bar().encode(
    x=alt.X('year(data_hora)'),
    y=alt.Y('count(data_hora)', sort='-x'),
    tooltip=['count(data_hora)', 'year(data_hora)'],

)

text1 = chart1.mark_text(
    align='center',
    baseline='middle',
    dx=26,
    dy=-15,
).encode(
    text=('count(data_hora)'),
)
st.altair_chart(chart1 + text1)
st.markdown("")

#Gráfico Top N de crimes registrados por bairro
st.markdown("**Top 15 de crimes registrados por bairro:**")
chart2 = alt.Chart(df).transform_aggregate(
    count='count()',
    groupby=['bairro']
).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('count', order='descending')]
).transform_filter(
    alt.datum.rank < 16
).mark_bar().encode(
    x='count:Q',
    y=alt.Y('bairro:N', sort='-x'),
    tooltip=['count:Q', 'bairro'],
    color='bairro:N',
)

text2 = chart2.mark_text(
    align='center',
    baseline='middle',
    dx=10,
).encode(
    text=('count:Q'),
)
st.altair_chart(chart2 + text2)
st.markdown("")

#Gráfico de crimes por horário de acontecimento
st.markdown("**Gráfico de crimes registrados por horário:**")
hist_values = np.histogram(df["data_hora"].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)
st.markdown("")

#Gráfico de quantidade de registro de boletim de ocorrência
st.markdown("**Gráfico de registro de boletim de ocorrência:**")
st.markdown("Onde 1 equivale a **registou** e 0 equivale a não **registrou**")
chart4 = alt.Chart(df).mark_bar().encode(
    x=alt.X('count(registrou_bo)', sort='-y'),
    y=alt.Y('registrou_bo:O'),
    tooltip=['count(registrou_bo)', 'registrou_bo'],
)

text4 = chart4.mark_text(
    align='center',
    baseline='middle',
    dx=26,
).encode(
    text=('count(registrou_bo)'),
)
st.altair_chart(chart4 + text4)
