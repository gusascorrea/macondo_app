import pandas as pd
import numpy as np
import streamlit as st


def segundos_para_hh_mm_ss(segundos_float):
    segundos = int(segundos_float)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return f'{horas:02d}:{minutos:02d}:{segundos:02d}'


def olx(pags, url, df_antigo):
    import requests
    from bs4 import BeautifulSoup

    import os

    @st.experimental_singleton
    def install_chromedriver():
        os.system('sbase install chromedriver')
        os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')

    _ = install_chromedriver()

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import time

    tempo = []
    start_time = time.time()

    with st.spinner('Inicializando...'):

        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        cookies = driver.find_element(
            By.XPATH, r'/html/body/div[2]/div/button')
        cookies.click()

    # Exemplo de uso:
    # Substitua isso pelo seu valor de tempo em segundos como float
    segundos_float = time.time() - start_time
    tempo.append(segundos_para_hh_mm_ss(segundos_float))

    st.write('Tempo de Inicialização:', tempo[0])

    # Executando WebCrawling

    start_time = time.time()

    st.markdown('---')


    with st.spinner('Buscando Anúncios...'):
        barra_prog = st.progress(0)
        count = 0
        lista = []
        pags = pags

        # Número de vezes que a página será rolada
        num_scrolls = 15

        for i in range(0, pags):
            # Obtém a altura total da página
            total_height = driver.execute_script(
                "return document.body.scrollHeight")

            # Calcula a altura de cada rolagem
            scroll_increment = total_height // num_scrolls

            # Realiza rolagens incrementais
            for j in range(num_scrolls + 5):
                for i in range(1, 56):
                    try:
                        link = driver.find_element(
                            By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/a').get_attribute('href')
                        descricao = driver.find_element(
                            By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[1]/div[1]/a/h2').text
                        preco = driver.find_element(
                            By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[1]/div[2]/h3').text
                        localizacao = driver.find_element(
                            By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[2]/div/div[2]/div[1]/p').text
                        data = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[2]/div/div[2]/div[2]/p').text

                        quartos = ''
                        area = ''
                        banheiros = ''
                        vagas = ''
                        iptu = ''
                        condominio = ''

                        # Loop para quartos
                        for c in range(1, 5):
                            try:
                                quartos_ = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[1]/div[1]/ul[1]/li[{c}]/span').get_attribute('aria-label')
                                if 'quarto' in quartos_:
                                    quartos = quartos_
                                    break
                            except Exception:
                                pass

                        # Loop para área
                        for c in range(1, 5):
                            try:
                                area_ = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[1]/div[1]/ul[1]/li[{c}]/span').get_attribute('aria-label')
                                if 'metro' in area_:
                                    area = area_
                                    break
                            except Exception:
                                pass

                        # Loop para banheiros
                        for c in range(1, 5):
                            try:
                                banheiros_ = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[1]/div[1]/ul[1]/li[{c}]/span').get_attribute('aria-label')
                                if 'banheiro' in banheiros_:
                                    banheiros = banheiros_
                                    break
                            except Exception:
                                pass

                        # Loop para vagas
                        for c in range(1, 5):
                            try:
                                vagas_ = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[4]/div[{i}]/section/div[2]/div[1]/div[1]/ul[1]/li[{c}]/span').get_attribute('aria-label')
                                if 'vaga' in vagas_:
                                    vagas = vagas_
                                    break
                            except Exception:
                                pass

                        # Loop para IPTU
                        for b in range(1, 3):
                            try:
                                iptu_ = driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/main/div/div[2]/main/div[4]/div[{i}]/section/div[2]/div[1]/div[2]/div/p[{b}]').text
                                if 'IPTU' in iptu_:
                                    iptu = iptu_
                                    break
                            except Exception:
                                pass

                        # Loop para Condomínio
                        for b in range(1, 3):
                            try:
                                condominio_ = driver.find_element(
                                    By.XPATH, f'/html/body/div[1]/div[1]/main/div/div[2]/main/div[4]/div[{i}]/section/div[2]/div[1]/div[2]/div/p[{b}]').text
                                if 'Condomínio' in condominio_:
                                    condominio = condominio_
                                    break
                            except Exception:
                                pass

                        lista.append([link, descricao, quartos, area, banheiros,
                                    vagas, preco, iptu, condominio, localizacao, data])

                    except Exception:
                        pass

                # Calcula a posição alvo para rolar
                scroll_to = j * scroll_increment

                # Executa o script para rolar até a posição desejada
                driver.execute_script("window.scrollTo(0, {});".format(scroll_to))

                # Aguarda um curto período para dar a impressão de rolagem gradual
                time.sleep(0.1)

            # Encontrar o botão
            if i < 1:
                button = driver.find_element(
                    By.XPATH, r'//*[@id="listing-pagination"]/aside/div/a[12]')
            elif i >= 1 and i < 9:
                button = driver.find_element(
                    By.XPATH, fr'//*[@id="listing-pagination"]/aside/div/a[{12 + i}]')
            else:
                button = driver.find_element(
                    By.XPATH, r'//*[@id="listing-pagination"]/aside/div/a[12]')

            # Utilizar JavaScript para rolar até o botão e clicar
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.1)
            button.click()
            count = count + (1/pags)
            try:
                barra_prog.progress(count)
            except:
                pass

    # Substitua isso pelo seu valor de tempo em segundos como float
    segundos_float = time.time() - start_time
    tempo.append(segundos_para_hh_mm_ss(segundos_float))

    st.write('Tempo de Busca:', tempo[1])
    st.write('Anúncios Buscados:', (pags*50))
    # Usando um conjunto para armazenar sublistas únicas
    sublistas_unicas = set(tuple(sublista) for sublista in lista)

    # Convertendo de volta para uma lista
    lista_sem_duplicatas = [list(sublista) for sublista in sublistas_unicas]
    aprov = (len(lista_sem_duplicatas)/(pags*50))*100
    st.write('Anúncios Únicos:', len(lista_sem_duplicatas),
             '(aproveitamento ', round(aprov, 2), '%)')

    df = pd.DataFrame(lista_sem_duplicatas)

    # Renomeando colunas
    df.columns = ['Link', 'Descricao', 'Quartos', 'Area', 'Banheiros', 'Vagas', 'Preco', 'IPTU', 'Condominio', 'Localizacao', 'Data']

    # Informações de colunas
    ## Descrição - criando classes
    # Lista de itens para verificar
    itens = ['casa em condominio', 'casa', 'apartamento', 'cobertura', 'loft', 'terreno', 'studio']

    # Função para encontrar o item correspondente na coluna e retornar o primeiro item encontrado
    def encontrar_item(texto):
        for item in itens:
            if item.lower() in texto.lower():
                return item
        return None

    # Aplicar a função encontrar_item à coluna e armazenar o resultado na nova coluna "Classe"
    df['Classe'] = df['Descricao'].apply(lambda x: encontrar_item(x))

    # Quartos
    df['Quartos'] = np.where(df.Quartos == '',np.nan,df.Quartos)

    # Replace NaN values with 0
    df['Quartos'] = df['Quartos'].fillna(0)

    # For other non-NaN values, take the first character of the string and convert it to int
    df['Quartos'] = df['Quartos'].astype(str).str[:1].astype(int)

    # Área
    df['Area'] = np.where(df.Area == '',np.nan,df.Area)

    # Remover 'm²' dos valores na coluna 'Area'
    df['Area'] = df['Area'].str.replace(' metros quadrados', '')
    df['Area'] = df['Area'].str.replace('.', '')
    df.Area = df.Area.astype(float)

    # Banheiros
    df['Banheiros'] = np.where(df.Banheiros == '',np.nan,df.Banheiros)

    # Replace NaN values with 0
    df['Banheiros'] = df['Banheiros'].fillna(0)

    # For other non-NaN values, take the first character of the string and convert it to int
    df['Banheiros'] = df['Banheiros'].astype(str).str[:1].astype(int)

    # Vagas

    df['Vagas'] = np.where(df.Vagas == '',np.nan,df.Vagas)

    # Replace NaN values with 0
    df['Vagas'] = df['Vagas'].fillna(0)

    # For other non-NaN values, take the first character of the string and convert it to int
    df['Vagas'] = df['Vagas'].astype(str).str[:1].astype(int)  

    # Preço - remover R$
    # Função para substituir os pontos
    def substituir_pontos(valor):
        if valor and valor[-2] != '.':
            valor = valor.replace('.', '')
        return valor

    # Aplicar a função às colunas do DataFrame
    df['Preco'] = df['Preco'].apply(substituir_pontos)

    # Remover R$
    df['Preco'] = df['Preco'].str[3:].astype(float)  

    # IPTU
    df['IPTU'] = np.where(df.IPTU == '',np.nan,df.IPTU)

    # Aplicar a função às colunas do DataFrame
    df['IPTU'] = df['IPTU'].str.replace('.', '')

    # Remover IPTU R$
    df['IPTU'] = df['IPTU'].str[8:].astype(float)

    # Condominio

    df['Condominio'] = np.where(df.Condominio == '',np.nan,df.Condominio)

    # Aplicar a função às colunas do DataFrame
    df['Condominio'] = df['Condominio'].str.replace('.', '')

    # Remover Condominio R$
    df['Condominio'] = df['Condominio'].str[14:].astype(float)     

    # Completando NaNs com 0
    df[['IPTU', 'Condominio']] = df[['IPTU', 'Condominio']].fillna(0)

    # Localização
    # Dividir os valores da coluna 'Localizacao' em 'Cidade' e 'Bairro'
    df[['Cidade', 'Bairro']] = df['Localizacao'].str.split(', ', expand=True)

    # Data
    import locale
    from datetime import datetime, timedelta

    # Define o locale para 'portuguese' (português)
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Mapear dias especiais ('Hoje' e 'Ontem') para datas reais
    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ontem = hoje - timedelta(days=1)

    # Obter o ano atual
    ano_atual = datetime.now().year

    # Mes atual
    mes_atual = datetime.now().month

    # Função para converter as datas especiais ('Hoje' e 'Ontem') para as datas reais
    def converter_data(texto):
        if pd.isna(texto):
            return np.nan  # Retornar NaN se a entrada for NaN

        if 'Hoje' in texto:
            return hoje
        elif 'Ontem' in texto:
            return ontem
        else:
            try:
                # Tente analisar a data
                if len(texto.split(',')) > 1:
                    return datetime.strptime(texto, '%d de %b, %H:%M')
                else:
                    # Modificação para considerar o ano anterior se o mês não for janeiro
                    data_formatada = datetime.strptime(f"{texto.strip()}, {ano_atual}", '%d de %b, %H:%M, %Y')
                    if data_formatada.month > mes_atual:  # Se o mês não for janeiro
                        data_formatada = data_formatada.replace(year=ano_atual - 1)  # Inserir o ano anterior
                    return data_formatada
            except ValueError:
                return np.nan  # Se não for possível analisar, retornar NaN

    # Aplicar a função converter_data à coluna 'Data'
    df['Data'] = df['Data'].astype(str).apply(converter_data)

    # Verificar se algum valor na coluna 'Data' é igual a '1900'
    if (df['Data'].dt.year == 1900).any():
        # Substituir os anos iguais a '1900' pelo ano atual
        df.loc[df['Data'].dt.year == 1900, 'Data'] = df.loc[df['Data'].dt.year == 1900, 'Data'].apply(lambda x: x.replace(year=ano_atual))
        
    if (df['Data'].dt.month > mes_atual).any():
        # Substituir os anos iguais a '1900' pelo ano atual
        df.loc[df['Data'].dt.month > mes_atual, 'Data'] = df.loc[df['Data'].dt.month != 1900, 'Data'].apply(lambda x: x.replace(year=ano_atual - 1))
        
        
    df = df.loc[~df['Data'].isna()]

    df['Ano'] = df['Data'].dt.year
    df['Mês'] = df['Data'].dt.month
    df['Dia'] = df['Data'].dt.day

    # Preço de aluguel
    if 'aluguel' in url:
        # Preço total de aluguel
        df['Preco'] = df['Preco'] + df['IPTU']/12 + df['Condominio']

        # Avaliar se aluguel é de temporada
        # Lista de itens para verificar
        itens = ['dia','temporada', 'diária']

        # Função para encontrar o item correspondente na coluna e retornar o primeiro item encontrado
        def encontrar_item(texto):
            for item in itens:
                if item.lower() in texto.lower():
                    return True
                else:
                    return False
            return None

        # Aplicar a função encontrar_item à coluna e armazenar o resultado na nova coluna "Classe"
        df['Temporada'] = df['Descricao'].apply(lambda x: encontrar_item(x))

        # Check if 'Temporada' exists in the DataFrame columns
        if 'Temporada' in df_antigo.columns:
            pass
        else:
            st.write("Arquivo antigo sem coluna 'Temporada', avalie se são dados de aluguel.")
        
    else:
        pass

    # Preco por metro quadrado
    df['Preco_por_m2'] = np.where(~df['Area'].isna(),\
                        round(df['Preco']/df['Area'],2),np.nan)
    
    # Ajuste de Bairros
    df['Bairro'] = np.where(df.Bairro == 'Tapera da Base', 'Tapera', df.Bairro)

    # Classificando Região

    bairros_central = [
        'Agronômica',
        'Centro',
        'Córrego Grande',
        'Itacorubi',
        'João Paulo',
        'José Mendes',
        'Monte Verde',
        'Pantanal',
        'Saco dos Limões',
        'Saco Grande',
        'Santa Mônica',
        'Trindade',
        'Carvoeira'
    ]

    bairros_continental = [
        'Balneário',
        'Bom Abrigo',
        'Capoeiras',
        'Coqueiros',
        'Estreito',
        'Itaguaçu',
        'Jardim Atlântico'
    ]

    bairros_leste = [
        'Lagoa da Conceição',
        'Barra da Lagoa',
        'São João do Rio Vermelho'
    ]

    bairros_norte = [
        'Cachoeira do Bom Jesus',
        'Cacupé',
        'Canasvieiras',
        'Daniela',
        'Ingleses do Rio Vermelho',
        'Jurerê Internacional',
        'Jurerê Tradicional',
        'Ponta das Canas',
        'Praia Brava',
        'Sambaqui',
        'Santo Antônio de Lisboa'
    ]

    bairros_sul = [
        'Armação do Pântano do Sul',
        'Campeche',
        'Carianos',
        'Costeira do Pirajubaé',
        'Morro das Pedras',
        'Pântano do Sul',
        'Ribeirão da Ilha',
        'Rio Tavares',
        'Tapera'
    ]

    conditions = [
        df['Bairro'].isin(bairros_central),
        df['Bairro'].isin(bairros_continental),
        df['Bairro'].isin(bairros_leste),
        df['Bairro'].isin(bairros_norte),
        df['Bairro'].isin(bairros_sul)
    ]

    choices = ['Central', 'Continental', 'Leste', 'Norte', 'Sul']

    df['Regiao'] = np.select(conditions, choices, default='')

    df['ID'] = df['Link'].str[-10:]
    df.set_index('ID', inplace=True)

    # Mesclando os DataFrames
    merged_df = pd.concat([df, df_antigo])

    # Removendo dados duplicados
    merged_df = merged_df.drop_duplicates()


    st.write('Dados:')
    st.write(merged_df)




def f1(pags):

    # Importando bibliotecas

    import requests
    from bs4 import BeautifulSoup

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import time

    from selenium.webdriver.chrome.options import Options

    #

    tempo = []
    start_time = time.time()

    # Abrindo WebDriver

    with st.spinner('Inicializando...'):

        url = 'https://f1ciaimobiliaria.com.br/imoveis?status=venda'

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(3)
        cookies = driver.find_element(
            By.XPATH, r'//*[@id="cookie_action_close_header"]')
        cookies.click()

    # Exemplo de uso:
    # Substitua isso pelo seu valor de tempo em segundos como float
    segundos_float = time.time() - start_time
    tempo.append(segundos_para_hh_mm_ss(segundos_float))

    st.write('Tempo de Inicialização:', tempo[0])

    # Executando WebCrawling

    start_time = time.time()

    st.markdown('---')

    with st.spinner('Buscando Anúncios...'):
        barra_prog = st.progress(0)
        count = 0
        lista = []
        if pags == np.inf:
            elementos = driver.find_element(
                By.XPATH, f'//*[@id="main"]/div/div[1]/div[1]/div/div[1]/h1').text
            pags = int(float(elementos[:4])//10 + 1)
        else:
            pags = pags
        for i in range(0, pags):
            for j in range(1, 11):
                try:
                    link = driver.find_element(
                        By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/header/h3/a').get_attribute('href')
                    descricao = driver.find_element(
                        By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/header/h3/a').text
                    preco = driver.find_element(
                        By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[1]/div/span').text
                except Exception:
                    pass

                quartos = ''
                area = ''
                banheiros = ''
                vagas = ''
                classe = ''
                iptu = ''
                condominio = ''

                # Area
                for atribute in range(1, 7):
                    try:
                        area_ = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[1]').text
                        if 'Área' in area_:
                            area = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[2]').text
                            break
                    except Exception:
                        pass

                # Quartos
                for atribute in range(1, 7):
                    try:
                        quartos_ = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[1]').text
                        if 'Quartos' in quartos_:
                            quartos = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[2]').text
                            break
                    except Exception:
                        pass

                # Banheiros
                for atribute in range(1, 7):
                    try:
                        banheiros_ = driver.find_element(
                            By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[1]').text
                        if 'Banheiros' in banheiros_:
                            banheiros = driver.find_element(
                                By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[2]').text
                            break
                    except Exception:
                        pass

                # Vagas
                for atribute in range(1, 7):
                    try:
                        vagas_ = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[1]').text
                        if 'Garagens' in vagas_:
                            vagas = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[2]').text
                            break
                    except Exception:
                        pass

                # Classe
                for atribute in range(1, 7):
                    try:
                        classe_ = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[1]').text
                        if 'Tipo' in classe_:
                            classe = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[1]/article[{j}]/div[2]/div/div[{atribute}]/div/span[2]').text
                            break
                    except Exception:
                        pass

                # iptu, condominio, localizacao, data])
                lista.append([link, descricao, quartos, area,
                            banheiros, vagas, classe, preco])

            # Encontrar o botão
            try:
                button = driver.find_element(
                    By.CSS_SELECTOR, r'#main > div > div.col-md-9 > div.pagination > a.next.page-numbers')
            except Exception:
                break

            # Utilizar JavaScript para rolar até o botão e clicar
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.1)
            button.click()
            count = count + (1/pags)
            try:
                barra_prog.progress(count)
            except:
                pass

    # Substitua isso pelo seu valor de tempo em segundos como float
    segundos_float = time.time() - start_time
    tempo.append(segundos_para_hh_mm_ss(segundos_float))

    st.write('Tempo de Busca:', tempo[1])
    st.write('Anúncios Buscados:', len(lista))
    # Usando um conjunto para armazenar sublistas únicas
    sublistas_unicas = set(tuple(sublista) for sublista in lista)

    # Convertendo de volta para uma lista
    lista_sem_duplicatas = [list(sublista) for sublista in sublistas_unicas]
    aprov = (len(lista_sem_duplicatas)/len(lista))*100
    st.write('Anúncios Únicos:', len(lista_sem_duplicatas),
             '(aproveitamento ', round(aprov, 2), '%)')

    df = pd.DataFrame(lista_sem_duplicatas)

    df.columns = ['Link', 'Descricao', 'Quartos',
                  'Area', 'Banheiros', 'Vagas', 'Classe', 'Preco']

    st.write(df)


def vivareal(pags):
    p = 1


def busca_dados():
    uploaded_file = st.sidebar.file_uploader(
        "Escolha um arquivo CSV ou Excel para mesclar com os dados buscados", type=["csv", "xlsx"])
    
    # Verifica se o arquivo foi carregado
    if uploaded_file is not None:
        # Verifica o tipo de arquivo e lê
        if uploaded_file.name.endswith('.csv'):
            df_antigo = pd.read_csv(uploaded_file, sep=';', index_col=0)
        elif uploaded_file.name.endswith('.xlsx'):
            df_antigo = pd.read_excel(uploaded_file, engine='openpyxl', index_col=0)
    else:
        # Define column names
        columns = ['Link', 'Descricao', 'Quartos', 'Area', 'Banheiros', 'Vagas',
                'Preco', 'IPTU', 'Condominio', 'Localizacao', 'Data', 'Classe',
                'Cidade', 'Bairro', 'Ano', 'Mês', 'Dia', 'Preco_por_m2', 'Regiao']

        # Create an empty DataFrame with the specified columns
        df_antigo = pd.DataFrame(columns=columns)
    
    imobs = ['OLX', 'F1', 'Viva Real']
    selec_imob = st.selectbox(
        'Selecione a imobiliária que deseja buscar os dados:', imobs)
    id_pag = ['Número específico de páginas', 'Todas as páginas']
    selec_pag = st.radio('Método de seleção de páginas:', id_pag)
    if selec_pag == 'Número específico de páginas':
        pags = st.number_input(
            'Páginas para a busca (Aperte Enter para Avançar):', min_value=1, value=1)
    else:
        pags = np.inf
        if selec_imob == 'OLX':
            st.write('Máximo de páginas: 100')
            pags = 100
    if selec_imob == 'OLX':
        url = st.text_input('Insira aqui o link de busca:', value = 'https://www.olx.com.br/imoveis/venda/estado-sc/florianopolis-e-regiao',
                             help = 'Procure criar filtros de busca que contenham no mínimo 500 anúncios e no máximo 5000 anúncios.')

    run = st.button('Buscar')

    if run:
        if selec_imob == 'OLX':
            st.markdown('---')
            olx(pags, url, df_antigo)

        elif selec_imob == 'F1':
            f1(pags)
        elif selec_imob == 'Viva Real':
            st.markdown('---')
            st.write('Em desenvolvimento')
            vivareal(pags)


def analise_dados():
    import plotly.express as px
    import plotly.graph_objects as go
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    # Widget para upload de arquivo
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
        bairros = df['Bairro'].unique()
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

        # Modelo de Regressão Linear

        # Criando o modelo de regressão linear
        X = filtered_df[['Area']]
        y = filtered_df['Preco']
        model = LinearRegression()
        model.fit(X, y)

        # Fazendo previsões
        predictions = model.predict(X)

        # Adicionando as previsões ao DataFrame
        filtered_df['Previsões'] = predictions

        # Calculando os erros (resíduos)
        errors = y - predictions
        filtered_df['Erro do Modelo'] = errors

        cor = st.selectbox('Coloração por:', ['Bairro', 'Regiao'])

        # Criando o gráfico de dispersão com Plotly
        fig = px.scatter(filtered_df, x='Area', y='Preco_por_m2', color=cor,
                         title='Gráfico de Dispersão: Área vs. Preço por m²',
                         labels={
                             'Area': 'Área [m²]', 'Preco_por_m2': 'Preço por m² [R$/m²]'},
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

        # Mostrando o gráfico no Streamlit
        st.plotly_chart(fig)

        # Criando o gráfico de dispersão com Plotly
        fig = px.scatter(filtered_df, x='Area', y='Preco', color=cor,
                         title='Gráfico de Dispersão: Área vs. Preço',
                         labels={'Area': 'Área [m²]', 'Preco': 'Preço [R$]'},
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
        fig.add_scatter(x=filtered_df['Area'], y=filtered_df['Previsões'],
                        mode='lines', name='Linha de Regressão',
                        line=dict(color='black', width=3))

        # Mostrando o gráfico no Streamlit
        st.plotly_chart(fig)

        # Tabela com os dados
        st.write(filtered_df[['Link', 'Area', 'Preco',
                 'Bairro', 'Previsões', 'Erro do Modelo']])

        # Calcular a média de Preço por metro quadrado e os desvios padrão por bairro
        media_preco_por_bairro = filtered_df.groupby(
            'Bairro')['Preco_por_m2'].mean()
        std_preco_por_bairro = filtered_df.groupby(
            'Bairro')['Preco_por_m2'].std()

        # Criar DataFrame com média e desvio padrão
        data = pd.DataFrame({'Bairro': media_preco_por_bairro.index,
                             'Media_Preco_por_m2': media_preco_por_bairro.values,
                             'Std_Preco_por_m2': std_preco_por_bairro.values})

        # Ordenar do maior ao menor
        data = data.sort_values(by='Media_Preco_por_m2', ascending=False)

        # Criar o gráfico de barras com barras de erro usando Plotly Express
        fig = px.scatter(data, x='Bairro', y='Media_Preco_por_m2',
                         error_y='Std_Preco_por_m2',
                         title='Média de Preço por m² por Bairro',
                         labels={
                             'Media_Preco_por_m2': 'Média de Preço por m²', 'Bairro': 'Bairro'},
                         color='Bairro',
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

        # Calcular a média de Preço por metro quadrado e os desvios padrão por classe
        media_preco_por_classe = filtered_df.groupby(
            'Classe')['Preco_por_m2'].mean()
        std_preco_por_classe = filtered_df.groupby(
            'Classe')['Preco_por_m2'].std()

        # Criar DataFrame com média e desvio padrão
        data = pd.DataFrame({'Classe': media_preco_por_classe.index,
                             'Media_Preco_por_m2': media_preco_por_classe.values,
                             'Std_Preco_por_m2': std_preco_por_classe.values})

        # Ordenar do maior ao menor
        data = data.sort_values(by='Media_Preco_por_m2', ascending=False)

        # Criar o gráfico de barras com barras de erro usando Plotly Express
        fig = px.scatter(data, x='Classe', y='Media_Preco_por_m2',
                         error_y='Std_Preco_por_m2',
                         title='Média de Preço por m² por Classe',
                         labels={
                             'Media_Preco_por_m2': 'Média de Preço por m²', 'Classe': 'Classe'},
                         color='Classe',
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

        # List of numerical features to consider for scatter plots
        numerical_features = ['Area', 'Quartos',
                              'Vagas', 'Preco', 'Preco_por_m2']

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

        # Criando o histograma para 'Preco_por_m2'
        histogram_preco_por_m2 = go.Histogram(
            x=filtered_df['Preco_por_m2'],
            histnorm='probability',
            name='Preco_por_m2 Histogram',
            marker=dict(color='#800000')
        )

        # Criando o histograma para 'Preco'
        histogram_preco = go.Histogram(
            x=filtered_df['Preco'],
            histnorm='probability',
            name='Preco Histogram',
            marker=dict(color='#008000')
        )

        # Média e Mediana para 'Preco_por_m2'
        mean_preco_por_m2 = filtered_df['Preco_por_m2'].mean()
        median_preco_por_m2 = filtered_df['Preco_por_m2'].median()

        # Média e Mediana para 'Preco'
        mean_preco = filtered_df['Preco'].mean()
        median_preco = filtered_df['Preco'].median()

        # Criando a figura para o primeiro histograma (Preco_por_m2)
        fig1 = go.Figure(data=[histogram_preco_por_m2])

        # Adicionando linhas verticais para a média e mediana com legendas
        fig1.add_vline(x=mean_preco_por_m2, line=dict(
            color="black", width=2, dash='dash'), name="Média")
        fig1.add_vline(x=median_preco_por_m2, line=dict(
            color="darkgrey", width=2, dash='dash'), name="Mediana")

        fig1.update_layout(
            title='Histograma de Preço/m²',
            xaxis=dict(title='Preço/m²'),
            yaxis=dict(title='Probabilidade')
        )

        # Criando a figura para o segundo histograma (Preco)
        fig2 = go.Figure(data=[histogram_preco])

        # Adicionando linhas verticais para a média e mediana com legendas
        fig2.add_vline(x=mean_preco, line=dict(
            color="black", width=2, dash='dash'), name="Média")
        fig2.add_vline(x=median_preco, line=dict(
            color="darkgrey", width=2, dash='dash'), name="Mediana")

        fig2.update_layout(
            title='Histograma de Preço',
            xaxis=dict(title='Preço'),
            yaxis=dict(title='Probabilidade')
        )

        # Organizando os gráficos na mesma linha
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)


def disp_anuncios():

    uploaded_file = st.sidebar.file_uploader(
        "Escolha um arquivo CSV ou Excel", type=["csv", "xlsx"])
    
    check = st.sidebar.button('Avaliar se anúncios estão disponíveis')

    if check:
        if uploaded_file is None:
            #st.sidebar.markdown('---')
            st.sidebar.write('*Insira um arquivo com dados para análise')
        else:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import Select
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            lista = []

            df_h = filtered_df.head(100)

            df_h['Valido'] = 1

            # Configuração do Selenium
            options = webdriver.ChromeOptions()
            options.add_argument('headless')  # Execução sem interface gráfica
            driver = webdriver.Chrome(options=options)

            for index, row in df_h.iterrows():
                link = row['Link']
                try:
                    driver.get(link)
                    # Verificar se o link é válido (sem erros no carregamento da página)
                    # Se não houver exceção, consideramos o link válido
                    pag_not_found = driver.find_element(
                        By.XPATH, r'//*[@id="root"]/div/div[1]/div[2]/div[2]/div[2]/span').text
                    if pag_not_found == 'A página não foi encontrada...':
                        df_h.loc[index, 'Valido'] = 0
                except Exception as e:
                    # Se ocorrer uma exceção (por exemplo, erro de carregamento), o link não é válido
                    pass

            driver.quit()  # Encerrar o driver após a conclusão

            # Exiba o DataFrame resultante
            st.write(df_h[['Link', 'Area', 'Preco', 'Bairro','Previsões', 'Erro do Modelo', 'Valido']])


def main():
    col1, col2, col3 = st.columns(3)

    with col2:
        st.title('Macondo')

    func = ['Início', #'Buscar Dados',
            'Análise de Dados',
            'Disponibilidade de Anúncios']
    funcao = st.sidebar.radio('Seção', func)

    if funcao == 'Buscar Dados':
        st.markdown('---')
        st.header('Buscar Dados')
        st.markdown('---')
        #busca_dados()
    elif funcao == 'Análise de Dados':
        st.markdown('---')
        st.header('Análise de Dados')
        st.markdown('---')
        analise_dados()
    elif funcao == 'Disponibilidade de Anúncios':
        st.markdown('---')
        st.header('Disponibilidade de Anúncios')
        st.markdown('---')
        st.write('Em Desenvolvimento')
        disp_anuncios()
    else:
        st.markdown('---')
        st.write('Aplicativo designado à busca e análise de anúncios de imóveis.')


main()
