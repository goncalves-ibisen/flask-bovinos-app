from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import json
import datetime
import math
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

app = Flask(__name__)

# Função para formatar valores com separador de milhar e casa decimal
def formatar_valor(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Carrega os dados do CSV
def carregar_dados_csv():
    try:
        dados = pd.read_csv('dados_animais.csv', header=0, sep=';')  # Substitua 'dados_animais.csv' pelo nome do seu arquivo CSV
        return dados
    except FileNotFoundError:
        print("Arquivo CSV não encontrado.")
        return None

# Função para consultar os dados do animal no CSV
# def consultar_animal(query, dados):
#     resultados = dados[(dados['nome'].str.contains(query, case=False, na=False)) | 
#                        (dados['registro'].astype(str).str.contains(query, case=False, na=False))]
    
#     if not resultados.empty:
#         return resultados.iloc[0].to_dict()  # Retorna o primeiro resultado encontrado como um dicionário
#     else:
#         return None

# Função para consultar os dados do animal no CSV
def consultar_animal(query, dados):
    resultados = dados[(dados['nome'].str.contains(query, case=False, na=False)) | 
                       (dados['registro'].astype(str).str.contains(query, case=False, na=False))]
    
    if not resultados.empty:
        resultado = resultados.iloc[0].to_dict()  # Retorna o primeiro resultado encontrado como um dicionário
        
        # Substituir valores NaN por um valor padrão apropriado
        for key, value in resultado.items():
            if isinstance(value, float) and math.isnan(value):  # Verifica se o valor é NaN
                resultado[key] = None  # Substitui NaN por None ou outro valor padrão

        return resultado
    else:
        return None
    
# Função para carregar os dados do CSV (supondo que já exista)
def carregar_dados_hist_preco():
    # Coloque aqui a lógica para carregar os dados
    df = pd.read_csv('dados/dados-historico-boi-gordo.csv', delimiter=';')
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
    df['valor-rs'] = pd.to_numeric(df['valor-rs'].str.replace(',', '.'), errors='coerce')
    return df

def totalizadores_dados(dados):    
    # Carregar o valor do arquivo JSON
    with open('valor_boi_hoje.json', 'r') as file:
        data = json.load(file)
        valor_boi = float(data['valor'].replace(',', '.'))  # Convertendo para float

    # Supondo que seu DataFrame se chame 'dados'
    # Verificar se a coluna 'valor' existe e, se sim, removê-la
    if 'valor' in dados.columns:
        dados = dados.drop(columns=['valor'])

    # Criar a nova coluna 'valor' multiplicando a coluna 'arrobas' pelo valor do arquivo JSON
    dados['valor'] = dados['arrobas'] * valor_boi
    
    total_animais = (dados[['registro']].count()).get('registro')
    total_arroba = (dados[['arrobas']].sum()).get('arrobas')
    total_avaliacao = round((dados[['valor']].sum()).get('valor'), 2)

    animais_sexo = dados['sexo'].value_counts()
    num_machos = animais_sexo.get('Macho', 0)
    num_femeas = animais_sexo.get('Femea', 0)

    num_bezerros = (dados[['classificacao']].value_counts()).get('Bezerro')
    num_garrotes = (dados[['classificacao']].value_counts()).get('Garrote')
    num_novilhos = (dados[['classificacao']].value_counts()).get('Novilho')
    num_boi = (dados[['classificacao']].value_counts()).get('Boi')
    num_prenhas = (dados[['prenha']].sum()).get('prenha')
    
    return {
        'total_animais': total_animais,
        'total_arroba': total_arroba,
        'total_avaliacao': total_avaliacao,
        'num_machos': num_machos,
        'num_femeas': num_femeas,
        'num_bezerros': num_bezerros,
        'num_garrotes': num_garrotes,
        'num_novilhos': num_novilhos,
        'num_boi': num_boi,
        'num_prenhas': num_prenhas
    }

@app.route('/')
def home():
    dados = carregar_dados_csv()
    totalizadores = totalizadores_dados(dados)
    
    dados_preco = carregar_dados_hist_preco()

    # Filtrar os dados para os últimos 30 dias
    last_days = datetime.now() - timedelta(days=20)
    df_last_days = dados_preco[dados_preco['data'] >= last_days]
    df_last_days = df_last_days.sort_values(by='data')

    # Gerar o gráfico e salvar como imagem
    plt.figure(figsize=(6, 4))  # Ajuste para um tamanho máximo de 420px
    plt.bar(df_last_days['data'].dt.strftime('%Y-%m-%d'), df_last_days['valor-rs'])
    plt.xlabel('Data')
    plt.ylabel('Valor (R$)')
    plt.title('Valores do Boi Gordo nos Últimos 30 Dias')
    plt.xticks(rotation=90)
    plt.tight_layout()
    image_path = 'static/grafico_boi_gordo.png'
    plt.savefig(image_path)

    return render_template('home.html', totalizadores=totalizadores, formatar_valor=formatar_valor, image_url=url_for('static', filename='/grafico_boi_gordo.png'))

@app.route('/consulta-animal', methods=['GET'])
def consulta_animal():
    query = request.args.get('query', '').strip()
    dados = carregar_dados_csv()

    if query:  # Verifica se a consulta não está vazia
        resultado = dados[dados['nome'].str.contains(query, case=False, na=False)]

        if not resultado.empty:
            animal = resultado.iloc[0].to_dict()
            return render_template('info-animal.html', animal=animal)
        else:
            return render_template('info-animal.html', animal=None, error='Animal não encontrado')
    else:
        return render_template('info-animal.html', animal=None, error='Por favor, insira um nome válido')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
