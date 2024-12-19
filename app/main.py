from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

def get_quote_currency(moeda_requerida:str, moeda_base:str):
    """ Busca o cambio mais atualizado da moeda requirida baseado na moeda base passadas como parametro e fazem uma requisição por meio de uma API
    Args: 
        moeda_requirida: Moeda para qual deseja saber o câmbio
        moeda_base: Moeda usada como comparação com a moeda requirida
    Return:
        response.json() (dict): retorna um dicionario com varias informações a cotação da moeda requirida em relação a moeda base
    """
    response = requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda_requerida}-{moeda_base}")
    return response.json()

def get_account_info_by_user_id(usuario_id: str):
    """Busca informações da conta do usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna informações da conta do usuário.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/Contas/usuario/{usuario_id}")
        return response.json()
    except:
        return "Não foi possível verificar as informações da conta no banco de dados :("
    
def get_investment_info_by_user_id(usuario_id: str):
    """Busca informações de investimentos do usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna informações de investimentos do usuário.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/Investimentos/usuario/{usuario_id}")
        return response.json()
    except:
        return "Não foi possível verificar as informações de investimentos no banco de dados :("
    
def get_uncontracted_products_by_user_id(usuario_id: str):
    """Busca produtos não contratados pelo usuário a partir do ID do usuário.
    Args:
        usuario_id: ID do usuário.
    Return:
        dict: Retorna um resumo dos produtos que a pessoa ainda não tem.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/ProdutosContratados/nao-contratados/usuario/{usuario_id}")
        response = response.json()
        prompt = f"Resuma esse json que possui informações sobre os produtos não contratados pelo usuário {response}"
        response_LLM = model.generate_content(prompt)
        return response_LLM.text
    except:
        return "Não foi possível verificar os produtos não contratados no banco de dados :("

def get_quote_value(valor: float, moeda_requerida: str, moeda_base: str):
    """Converte um valor da moeda base para a moeda requerida usando a cotação atual.
    Args:
        valor: Valor a ser convertido.
        moeda_requerida: Moeda para qual deseja saber o câmbio.
        moeda_base: Moeda usada como comparação com a moeda requerida.
    Return:
        dict: Retorna um dicionário com o valor convertido e a cotação utilizada.
    """
    cotacao = get_quote_currency(moeda_requerida, moeda_base)
    taxa_cambio = float(cotacao[f"{moeda_requerida}{moeda_base}"]["bid"])
    valor_convertido = valor * taxa_cambio
    return {
        "valor_convertido": valor_convertido,
        "taxa_cambio": taxa_cambio
    }

def transfer_to_human():
    """
    Args:
    return: 
        recado (string): recado de transferencia para um atendente humano
    """
    recado = "Deve transferir para um atendente humano"
    numero_protocolo = "123456"
    return recado, numero_protocolo

def get_user_id_by_email(email: str):
    """Busca o ID do usuário a partir do email.
    Args:
        email: Email do usuário.
    Return:
        str: Retorna o ID do usuário.
    """
    try:
        response = requests.get(f"http://172.17.0.1:7296/api/Usuarios/email/{email}/id")
        return response.json()
    except:
        return "Não foi possível verificar o email no banco de dados :("

def get_user_details(email: str):
    """Busca informações do usuário a partir do email.
    Args:
        email: Email do usuário.
    Return:
        dict: Retorna informações como nome, email, telefone, idade, gênero apenas. Caso o usuário queira, ele pode solicitar informações sobre contas e investimentos posteriormente.
    """
    user_id = get_user_id_by_email(email)
    if user_id:
        response = requests.get(f"http://172.17.0.1:7296/api/Usuarios/{user_id}")
        return response.json()
    else:
        return "Não foi possível encontrar o usuário com o email fornecido."

# def get_user_by_id(user_id:str):
#     """ Busca no banco de dados o usuario com o mesmo user_id
#     Args:
#         user_id: Número de identificação do usuário no banco de dados
#     Return:
#         response.json() (dict): Retorna informações como nome, email, telefone, idad, genero, contas, investimentos e produtos contratados pelo usuário
#     """
#     try:
#         response = requests.get(f"http://172.17.0.1:7296/api/Usuarios/{user_id}")
#         return response.json()
#     except:
#         return "Não foi possivel verificar essa pessoa no banco de dados :("
    
# def get_user_info_by_email(email: str):
#     """Busca informações do usuário a partir do email.
#     Args:
#         email: Email do usuário.
#     Return:
#         dict: Retorna informações como nome, email, telefone, idade, gênero, contas, investimentos e produtos contratados pelo usuário.
#     """
#     user_id = get_user_id_by_email(email)
#     if user_id:
#         user_info = get_user_by_id(user_id)
#         return user_info
#     else:
#         return "Não foi possível encontrar o usuário com o email fornecido."

def get_products(produtos:str):
    """Informa os produtos financeiros, de investimento ou bancários que o banco oferece.
    Args:
        produtos: argumento aleatório
    Return: 
        Retorna todos os produtos oferecidos pelo Banco.
    """
    response = requests.get("http://172.17.0.1:7296/api/ProdutosBancarios")
    response = response.json()
    prompt = f"Resuma esse json que possui informações sobre os produtos de um banco {response}"
    response_LLM = model.generate_content(prompt)
    return response_LLM.text


tool = [get_quote_currency, get_quote_value, transfer_to_human, get_user_id_by_email, get_user_details, get_products, get_account_info_by_user_id, get_investment_info_by_user_id, get_uncontracted_products_by_user_id]

genai.configure(api_key="AIzaSyCA8UFoADPrHVzFq26gFWtzqJ4IzyxfqRc")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    generation_config=generation_config,
    system_instruction="Seu nome é Agente Pinho e você é um assistente virtual do Banco Pine. Suas tarefas é responder os clientes de forma mais amigavel possível e conseguir resolver questões bancárias dos clientes do banco como consulta de saldo de conta, gerar os extratos bancários, informar cotação de moedas chamando a função get_quote_currency, informar sobre investimentos e sobre o mercado financeiro." 

    "Quando o usuário solicitar informações pessoais, você deve informar o nome, email, telefone, idade, gênero do usuário e também seu id, chamando a função get_user_info_by_email. Memorize o id da pessoa. A não ser que essas informações estejam no histórico da conversa. Porém, se a pessoa solicitar uma consulta nova, faça e informe os dados."

    "Quando o usuário solicitar informações sobre a conta, você deve informar o saldo da conta, chamando a função get_account_info_by_user_id. Caso não tenha o id, consiga o id pelo email do usuário."

    "Quando o usuário solicitar informações sobre investimentos, você deve informar os investimentos do usuário, chamando a função get_investment_info_by_user_id. Caso não tenha o id, consiga o id pelo email do usuário."

    "Quando o usuário solicitar informações sobre produtos não contratados, você deve informar os produtos não contratados pelo usuário, chamando a função get_uncontracted_products_by_user_id. Caso não tenha o id, consiga o id pelo email do usuário."

    "Quando o usuário solicitar informações de cotação ou câmbio, você deve sempre informar também a data e hora da cotação."

    "Você não deve inventar produtos ou informações sobre o banco. Você deve sempre buscar informações reais no banco de dados."

    "Quando o usuário solicitar a conversão de um valor de uma moeda para outra, você deve informar o valor convertido e a taxa de câmbio utilizada, chamar a função get_quote_value."

    "Alguns serviços terá que fazer chamadas de API externas como ver cotações e usuarios. Você não deve responder questões fora dos assuntos de mercado financeiro, transações ou serviços do Banco."

    "Quando um usuário solicitar informações sobre produtos, você deve informar todos os produtos oferecidos pelo Banco, por meio da função get_products."

    "Caso não consiga resolver a questão do cliente, você deve transferir para um atendente humano chamando a função transfer_to_human. Como resposta para o usuário, além de informar que a questão será resolvida por um atendente humano, você deve informar o número do protocolo da conversa e um resumo da conversa até o momento",
    tools=tool 
)

app = Flask(__name__)
history = []

@app.route('/mensagem', methods=['POST'])
def enviar_mensagem():
    mensagem = request.json.get('mensagem')
    if mensagem:
        chat_session = model.start_chat(
            history=history,
            enable_automatic_function_calling=True
        )
        response = chat_session.send_message(mensagem)
        resposta_text = response.text
        history.append({"role":"user","parts":[mensagem]})
        history.append({"role":"model","parts":[resposta_text]})
        return resposta_text, 200
    else:
        return jsonify({'erro': 'Mensagem não fornecida'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
