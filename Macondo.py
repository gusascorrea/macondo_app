import pandas as pd
import numpy as np
import streamlit as st


def segundos_para_hh_mm_ss(segundos_float):
    segundos = int(segundos_float)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return f'{horas:02d}:{minutos:02d}:{segundos:02d}'

def correlacao(filtered_df):
    import plotly.express as px
    import plotly.graph_objects as go
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    # List of numerical features to consider for scatter plots
    numerical_features = ['Area', 
                          'Quartos',
                          'Banheiros',
                          'Vagas',
                          'Preco',
                          'Preco_por_m2']

    # Compute the correlation matrix
    # You can extend this to more features if needed
    corr = filtered_df[numerical_features].corr()

    # Initialize a Matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 9))

    # Generate a heatmap using Seaborn
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)

    # Set title
    ax.set_title('Mapa de Calor - Correlação Linear')

    # Display the plot using Streamlit
    st.pyplot(fig)


def dispersao(filtered_df):

    import plotly.express as px
    import plotly.graph_objects as go
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    col1, col2 = st.columns(2)

    with col1:
        x = st.selectbox('Argumento X:', ['Area', 'Quartos','Banheiros', 'Vagas','Preco', 'Preco_por_m2'])

    with col2:
        y = st.selectbox('Argumento Y:', ['Preco', 'Preco_por_m2', 'Area', 'Quartos', 'Banheiros'])

    cor = st.selectbox('Coloração por:', ['Regiao', 'Bairro', 'Quartos','Banheiros', 'Vagas', 'Erro do Modelo'])

    st.markdown('---')

    # Correlação
    corr = filtered_df[x].corr(filtered_df[y])

    # Exibir o resultado
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f'Correlação linear entre {x} e {y}:',value = round(corr,2))  
    
    with col2:
        # Exibir o indicador de acordo com o valor da correlação
        if corr > 0.7:
            st.success('Correlação Forte')
        elif 0.5 <= corr <= 0.7:
            st.warning('Correlação Moderada')
        else:
            st.error('Correlação Fraca')
    
    # Modelo de Regressão Linear
    
    # Criando o modelo de regressão linear
    X = filtered_df[[x]]
    z = filtered_df[y]
    model = LinearRegression()
    model.fit(X, z)

    # Fazendo previsões
    predictions = model.predict(X)

    # Adicionando as previsões ao DataFrame
    filtered_df['Previsões'] = predictions

    # Calculando os erros (resíduos)
    errors = z - predictions
    filtered_df['Erro do Modelo'] = errors

    # Criando o gráfico de dispersão com Plotly
    fig = px.scatter(filtered_df, x=x, y=y, color=cor,
                        title=f'Gráfico de Dispersão: {x} vs. {y}',
                        labels={
                            f'{x}': f'{x}', f'{y}': f'{y}'},
                        hover_data={'Descricao': True},
                        width=900, height=600)

    # Adicionando texto de descrição e link a cada ponto
    fig.update_traces(text=filtered_df['Descricao'], hoverinfo='text')

    # Definindo a ação ao clicar no ponto
    fig.update_traces(marker=dict(size=12),
                        selector=dict(mode='markers'),
                        meta={'Link': 'Link'})

    # Aumentando o tamanho da fonte nos eixos x e y
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(size=17)  # Define o tamanho da fonte no eixo x
        ),
        yaxis=dict(
            tickfont=dict(size=17)  # Define o tamanho da fonte no eixo y
        ),
        title=dict(
            font=dict(size=20)  # Define o tamanho da fonte no título
        )
    )

    # Adicionando a linha de regressão
    fig.add_scatter(x=filtered_df[x], y=filtered_df['Previsões'],
                    mode='lines', name='Linha de Regressão',
                    line=dict(color='black', width=3))

    # Mostrando o gráfico no Streamlit
    st.plotly_chart(fig)

    # Tabela com os dados
    st.write(filtered_df[['Link', 'Area', 'Preco',
                'Bairro', 'Previsões', 'Erro do Modelo']])

def medias(filtered_df):

    import plotly.express as px
    import plotly.graph_objects as go
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    col1, col2 = st.columns(2)

    with col1:
        x = st.selectbox('Argumento X:', ['Regiao','Bairro', 'Classe', 'Area', 'Quartos','Banheiros', 'Vagas'])

    with col2:
        y = st.selectbox('Argumento Y:', ['Preco', 'Preco_por_m2', 'Area', 'Quartos','Banheiros', 'Vagas'])    

    # Calcular a média de Preço por metro quadrado e os desvios padrão por bairro
    media_x_por_y = filtered_df.groupby(
        x)[y].mean()
    std_x_por_y = filtered_df.groupby(
        x)[y].std()

    # Criar DataFrame com média e desvio padrão
    data = pd.DataFrame({x: media_x_por_y.index,
                            'Media_y': media_x_por_y.values,
                            'Std_y': std_x_por_y.values})

    # Ordenar do maior ao menor
    data = data.sort_values(by='Media_y', ascending=False)

    # Criar o gráfico de barras com barras de erro usando Plotly Express
    fig = px.scatter(data, x=x, y='Media_y',
                        error_y='Std_y',
                        title=f'Média de {y} por {x}',
                        labels={
                            'Media_y': f'Média de {y}', x: x},
                        color=x,
                        width=800, height=600)

    # Definir rotação dos rótulos do eixo x
    fig.update_layout(xaxis_tickangle=-45)

    # Aumentando o tamanho da fonte nos eixos x e y
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(size=17)  # Define o tamanho da fonte no eixo x
        ),
        yaxis=dict(
            tickfont=dict(size=17)  # Define o tamanho da fonte no eixo y
        ),
        title=dict(
            font=dict(size=20)  # Define o tamanho da fonte no título
        )
    )

    # Mostrar o gráfico no Streamlit
    st.plotly_chart(fig)

 

def histogramas(filtered_df):
    import plotly.express as px
    import plotly.graph_objects as go
    import seaborn as sns
    import matplotlib.pyplot as plt
    from scipy.stats import skew, kurtosis
    from sklearn.linear_model import LinearRegression

    x = st.selectbox('Argumento X:', ['Preco','Preco_por_m2', 'Area', 'Quartos','Banheiros', 'Vagas'])

    df_hist = filtered_df[x].dropna()

    # Criando o histograma para 'x'
    histogram_preco_por_m2 = go.Histogram(
        x=df_hist,
        histnorm='probability',
        name=f'{x} Histogram',
        marker=dict(color='#800000')
    )

    # Skewness
    skew_df_hist = skew(df_hist)

    # Curtosis
    curtosis_df_hist = kurtosis(df_hist)

    # Média e Mediana para 'x'

    st.markdown('---')

    col1, col2, col3 = st.columns(3)


    mean_x = df_hist.mean()
    median_x = df_hist.median()
    std_x = df_hist.std()

    with col1:
        st.metric('Média',round(mean_x,0))

    with col2:
        st.metric('Mediana',round(median_x,0))

    with col3:
        st.metric('Desvio Padrão', round(std_x,0))

    col1, col2,col3,col4,col5 = st.columns(5)

    with col2:
        st.metric('Skewness', round(skew_df_hist,2), help = 'Medida da falta de simetria de uma determinada distribuição de frequência.')

    with col4:
        st.metric('Curtosis', round(curtosis_df_hist,2), help = 'Medida de forma que caracteriza o achatamento da curva da função de distribuição de probabilidade.')

    # Criando a figura para o primeiro histograma (Preco_por_m2)
    fig1 = go.Figure(data=[histogram_preco_por_m2])

    # Adicionando linhas verticais para a média e mediana com legendas
    fig1.add_vline(x=mean_x, line=dict(
        color="black", width=2, dash='dash'), name="Média")
    fig1.add_vline(x=median_x, line=dict(
        color="darkgrey", width=2, dash='dash'), name="Mediana")
    fig1.add_vline(x=mean_x + std_x, line=dict(
        color="blue", width=2, dash='dash'), name="Mediana")
    fig1.add_vline(x=mean_x - std_x, line=dict(
        color="blue", width=2, dash='dash'), name="Mediana")

    fig1.update_layout(
        title=f'Histograma de {x}',
        xaxis=dict(title=f'{x}'),
        yaxis=dict(title='Probabilidade')
    )

    # Organizando os gráficos na mesma linha
    st.plotly_chart(fig1, use_container_width=True)

def main():
    col1, col2, col3 = st.columns(3)

    with col2:
        st.title('Macondo')

    # Widget para upload de arquivo
    st.sidebar.title('Macondo')
    st.sidebar.markdown('---')
    uploaded_file = st.sidebar.file_uploader(
        "Escolha um arquivo CSV ou Excel", type=["csv", "xlsx"])

    # Verifica se o arquivo foi carregado
    if uploaded_file is not None:
        # Verifica o tipo de arquivo e lê
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep=';', index_col=0)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl', index_col=0)

        if len(df.columns) == 0:
            df = pd.read_csv(uploaded_file, index_col=0)


        func = ['Início',
                'Correlação',
                'Dispersões',
                'Médias',
                'Histogramas']
        funcao = st.sidebar.radio('Seção', func)

        # Filtro de área na sidebar
        st.sidebar.markdown('---')
        st.sidebar.title('Filtros:')

        # Filtrando por Região
        regioes = df['Regiao'].unique()
        regioes_selecionadas = st.sidebar.multiselect(
            'Selecione a(s) Região(ões)', regioes)

        # Filtrando os dados
        filtered_df = df[df['Regiao'].isin(
            regioes_selecionadas)] if regioes_selecionadas else df

        # Filtrando por bairro
        bairros = filtered_df['Bairro'].unique()
        bairros_selecionados = st.sidebar.multiselect(
            'Selecione o(s) Bairro(s)', bairros)

        # Filtrando os dados
        filtered_df = filtered_df[filtered_df['Bairro'].isin(
            bairros_selecionados)] if bairros_selecionados else filtered_df

        # Filtrando por classe
        classes = df['Classe'].unique()
        classes_selecionadas = st.sidebar.multiselect(
            'Selecione a(s) Classe(s)', classes)

        # Filtrando os dados
        filtered_df = filtered_df[filtered_df['Classe'].isin(
            classes_selecionadas)] if classes_selecionadas else filtered_df

        # Organizando os inputs na mesma linha
        col1, col2 = st.sidebar.columns(2)

        with col1:
            min_area = st.number_input(
                'Área mínima [m²]', min_value=0, value=0)

        with col2:
            max_area = st.number_input(
                'Área máxima [m²]', min_value=min_area, value=200)

        # Organizando os inputs na mesma linha
        col1, col2 = st.sidebar.columns(2)

        with col1:
            min_pm2 = st.number_input(
                'Limite inferior de Preço/m² [R$/m²]', min_value=0, value=0)

        with col2:
            max_pm2 = st.number_input(
                'Limite superior de Preço/m² [R$/m²]', min_value=min_pm2, value=40000)

        # Organizando os inputs na mesma linha
        col1, col2 = st.sidebar.columns(2)

        with col1:
            min_p = st.number_input(
                'Limite inferior de Preço [R$]', min_value=0, value=0)

        with col2:
            max_p = st.number_input(
                'Limite superior de Preço [R$]', min_value=min_p, value=100000000)

        # Defina o valor mínimo e máximo de quartos no DataFrame
        min_quartos = int(filtered_df['Quartos'].min())
        max_quartos = int(filtered_df['Quartos'].max())

        # Crie um range slider para selecionar o intervalo de número de quartos
        min_quartos_selected, max_quartos_selected = st.sidebar.slider('Número de quartos',
                                                                       min_value=min_quartos,
                                                                       max_value=max_quartos,
                                                                       value=(min_quartos, max_quartos))

        # Defina o valor mínimo e máximo de quartos no DataFrame
        min_vagas = int(filtered_df['Vagas'].min())
        max_vagas = int(filtered_df['Vagas'].max())

        # Crie um range slider para selecionar o intervalo de número de quartos
        min_vagas_selected, max_vagas_selected = st.sidebar.slider('Número de vagas',
                                                                   min_value=min_vagas,
                                                                   max_value=max_vagas,
                                                                   value=(min_vagas, max_vagas))

        # Filtrando os dados
        filtered_df = filtered_df[(filtered_df['Area'] >= min_area) & (filtered_df['Area'] <= max_area)
                                  & (filtered_df['Preco_por_m2'] >= min_pm2) & (filtered_df['Preco_por_m2'] <= max_pm2)
                                  & (filtered_df['Preco'] >= min_p) & (filtered_df['Preco'] <= max_p)
                                  & (filtered_df['Quartos'] >= min_quartos_selected) & (filtered_df['Quartos'] <= max_quartos_selected)
                                  & (filtered_df['Vagas'] >= min_vagas_selected) & (filtered_df['Vagas'] <= max_vagas_selected)]

        if funcao == 'Correlação':
            st.markdown('---')
            st.header('Correlação')
            st.markdown('---')
            correlacao(filtered_df)
        elif funcao == 'Dispersões':
            st.markdown('---')
            st.header('Dispersões')
            st.markdown('---')
            dispersao(filtered_df)            
        elif funcao == 'Médias':
            st.markdown('---')
            st.header('Médias')
            st.markdown('---')
            medias(filtered_df)
        elif funcao == 'Histogramas':
            st.markdown('---')
            st.header('Histogramas')
            st.markdown('---')
            histogramas(filtered_df)
        else:
            st.markdown('---')
            st.write('Aplicativo designado à análise de anúncios de imóveis.')


main()
