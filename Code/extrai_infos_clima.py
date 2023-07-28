from os.path import join
import os
import pandas as pd
from datetime import datetime
import mysql.connector
import schedule
import time
import configparser

def criar_banco(host,user,password):
    try:
        # Conectando ao servidor MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        #objeto SQL
        cursor = connection.cursor()

        cursor.execute('CREATE DATABASE IF NOT EXISTS clima;')
        print("Banco de dados 'clima' criado com sucesso!")

        cursor.execute("USE clima;")

        cursor.execute(
        '''CREATE TABLE IF NOT EXISTS climate_data (
            ID SMALLINT AUTO_INCREMENT PRIMARY KEY,
            capital varchar(100),
            UF char(2),
            datetime DATE DEFAULT CURRENT_TIMESTAMP,
            tempmax DECIMAL(6,2),
            tempmin DECIMAL(6,2),
            feelslikemax DECIMAL(6,2),
            feelslikemin DECIMAL(6,2),
            feelslike DECIMAL(6,2),
            humidity DECIMAL(6,2),
            precip DECIMAL(6,2),
            precipprob DECIMAL(6,2),
            precipcover DECIMAL(6,2),
            preciptype VARCHAR(20),
            windgust DECIMAL(6,2),
            windspeed DECIMAL(6,2),
            winddir DECIMAL(6,2),
            sealevelpressure DECIMAL(6,2),
            cloudcover DECIMAL(6,2),
            visibility DECIMAL(6,2),
            solarradiation DECIMAL(6,2),
            solarenergy DECIMAL(6,2),
            uvindex TINYINT,
            severerisk TINYINT,
            sunrise DATETIME,
            sunset DATETIME,
            moonphase DECIMAL(4,2),
            conditions varchar(100),
            description varchar(100),
            icon varchar(100),
            stations varchar(100)
            );'''
        )
        print("Tabela 'climate_data' criado com sucesso")
    
    except mysql.connector.Error as err:
        print(f"Erro ao criar o banco de dados: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("tarefa 'criar-banco' foi encerrada.")
            print('*'*50)

def tratar_dados(dados):
        dados['capital']            = dados['name'].apply(lambda x: x.split(',')[0])[0].strip()
        dados['UF']                 = dados['name'].apply(lambda x: x.split(',')[1])[0].strip()
        dados['tempmax']            = round(float(dados['tempmax'].iloc[0]),2)
        dados['windgust']           = round(float(dados['tempmin'].iloc[0]),2)
        dados['feelslikemax']       = round(float(dados['feelslikemax'].iloc[0]),2)
        dados['feelslikemin']       = round(float(dados['feelslikemin'].iloc[0]),2)
        dados['feelslike']          = round(float(dados['feelslike'].iloc[0]),2)
        dados['humidity']           = round(float(dados['humidity'].iloc[0]),2)
        dados['precip']             = round(float(dados['precip'].iloc[0]),2)
        dados['precipprob']         = round(float(dados['precipprob'].iloc[0]),2)
        dados['precipcover']        = round(float(dados['precipcover'].iloc[0]),2)
        dados['preciptype']         = str(dados['preciptype'].iloc[0]) # Chuva, Neve, Chuva gelada e gelo
        dados['windgust']           = round(float(dados['windgust'].iloc[0]),2)
        dados['windspeed']          = round(float(dados['windspeed'].iloc[0]),2)
        dados['winddir']            = round(float(dados['winddir'].iloc[0]),2)
        dados['sealevelpressure']   = round(float(dados['sealevelpressure'].iloc[0]),2)
        dados['cloudcover']         = round(float(dados['cloudcover'].iloc[0]),2)
        dados['visibility']         = round(float(dados['visibility'].iloc[0]),2)
        dados['solarradiation']     = round(float(dados['solarradiation'].iloc[0]),2)
        dados['solarenergy']        = round(float(dados['solarenergy'].iloc[0]),2)
        dados['uvindex']            = int(dados['uvindex'].iloc[0])
        dados['severerisk']         = int(dados['severerisk'].iloc[0])
        dados['sunrise']            = datetime.strptime(dados['sunrise'].iloc[0],"%Y-%m-%dT%H:%M:%S")
        dados['sunset']             = datetime.strptime(dados['sunset'].iloc[0],"%Y-%m-%dT%H:%M:%S")
        dados['moonphase']          = round(float(dados['moonphase'].iloc[0]),2)
        dados['conditions']         = str(dados['conditions'].iloc[0])
        dados['description']        = str(dados['description'].iloc[0])
        dados['icon']               = str(dados['icon'].iloc[0])
        dados['stations']           = str(dados['stations'].iloc[0]) 

        del dados['name']
        del dados['snow'] # Deletando as informações de neve
        del dados['snowdepth'] # Deletando as informações de neve
        dados.reset_index(drop=True,inplace=True)
        return dados

def conectar_api(key,cidades):
    df_suporte = pd.DataFrame()
    data_extracao = datetime.today().strftime('%Y-%m-%d') # formatando as datas
    for cidade in cidades:
        try:
            URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
                f'{cidade}/{data_extracao}/?unitGroup=metric&include=days&key={key}&contentType=csv')
        except:
            print(f'Erro na extração dos dados da {cidade}')
        dados = tratar_dados(pd.read_csv(URL))
        df_suporte = pd.concat([df_suporte,dados])
    print("tarefa 'conectar_api' foi encerrada.")
    print(f"Total de registros: {len(df_suporte.index)}")
    print('*'*50)
    return df_suporte

def inserir_banco(host,user,password,dados):
    try:
        # Conectando ao servidor MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        #objeto SQL
        cursor = connection.cursor()   
        cursor.execute("USE clima;")    
        for _, linha in dados.iterrows():
            insert_query = f"""
                INSERT INTO climate_data (capital,UF,datetime,tempmax,tempmin,feelslikemax,
                    feelslikemin,feelslike,humidity,precip,precipprob,precipcover,preciptype,
                    windgust,windspeed,winddir,sealevelpressure,cloudcover,visibility,
                    solarradiation,solarenergy,uvindex,severerisk,sunrise,sunset,moonphase,conditions,
                    description,icon,stations)
                VALUES 
                    ("{linha['capital']}","{linha['UF']}","{linha['datetime']}","{linha['tempmax']}",
                    "{linha['tempmin']}","{linha['feelslikemax']}","{linha['feelslikemin']}",
                    "{linha['feelslike']}","{linha['humidity']}","{linha['precip']}","{linha['precipprob']}",
                    "{linha['precipcover']}","{linha['preciptype']}",{linha['windgust']},"{linha['windspeed']}",
                    "{linha['winddir']}","{linha['sealevelpressure']}","{linha['cloudcover']}",
                    "{linha['visibility']}","{linha['solarradiation']}","{linha['solarenergy']}",
                    "{linha['uvindex']}","{linha['severerisk']}","{linha['sunrise']}","{linha['sunset']}",
                    "{linha['moonphase']}","{linha['conditions']}","{linha['description']}","{linha['icon']}","{linha['stations']}")"""
            cursor.execute(insert_query)
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao inserir os dados: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("tarefa 'inserir_banco' foi encerrada.")
            print('*'*50)

if __name__ == "__main__":
    host_mysql = 'localhost'         # Declaração do Host Mysql
    user_mysql = 'xadia'
    password_mysql = "variavel_ansible_user_pass"
    key_API = "variavel_ansible_api"
    lista_cidades = ['RioBranco,AC','Maceio,AL','Macapa,AP','Manaus,AM','Salvador,BA','Fortaleza,CE','Vitoria,ES','Goiania,GO',
             'SaoLuis,MA','Cuiaba,MT','CampoGrande,MS','BeloHorizonte,MG','Belem,PA','JoaoPessoa,PB','Curitiba,PR','Recife,PE','Teresina,PI',
             'RiodeJaneiro,RJ','Natal,RN','PortoAlegre,RS','PortoVelho,RO','BoaVista,RR','Florianopolis,SC','SaoPaulo,SP','Aracaju,SE','Palmas,TO'] # Lista de cidades para a busca
    criar_banco(host_mysql,user_mysql,password_mysql)

    def schedule_job(): # Função responsável por ativar todos os pasos do código aguardando a permissão do schedule 
        extracao_dia = conectar_api(key_API,lista_cidades)
        inserir_banco(host_mysql,user_mysql,password_mysql,extracao_dia)

    schedule.every().day.at("12:05").do(schedule_job)
    while True:
        schedule.run_pending()
        time.sleep(1)