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

# def transfer_to_human():
#     """
#     Args:
#     return: 
#         recado (string): recado de transferencia para um atendente humano
#     """
#     recado = "Deve transferir para um atendente humano"
#     return recado

def get_user_by_id(user_id:str):
    """ Busca no banco de dados o usuario com o mesmo user_id
    Args:
        user_id: Número de identificação do usuário no banco de dados
    Return:
        response.json() (dict): Retorna informações como nome, email, telefone, idad, genero, contas, investimentos e produtos contratados pelo usuário
    """
    try:
      response = requests.get(f"http://localhost:7296/api/Usuarios/{user_id}")
      return response.json()
    except:
      return "Não foi possivel verificar essa pessoa no banco de dados :("

def get_products(produtos:str):
    """Informa os produtos de investimento que o banco oferece
    Args:
      produtos: argumento aleatório
    Return: 
      Retorna todos os produtos de investimento oferecidos pelo Banco
    """
    response = requests.get("http://localhost:7296/api/ProdutosBancarios")
    response = response.json()
    prompt = f"Resuma esse json que possui informações sobre os produtos de um banco {response}"
    response_LLM = model.generate_content(prompt)
    return response_LLM.text


tool = [get_quote_currency, get_user_by_id, get_products]

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
    system_instruction="""Seu nome é Agente Pinho e você é um assistente virtual do Banco Pine. Suas tarefas é responder os clientes de forma mais amigavel possível e conseguir resolver questões bancárias dos clientes do banco como consulta de saldo de conta, gerar os extratos bancários, informar cotação de moedas chamando a função get_quote_currency, informar sobre investimentos e sobre o mercado financeiro. Alguns serviços terá que fazer chamadas de API externas como ver cotações e usuarios. Você não deve responder questões fora dos assuntos de mercado financeiro, transações ou serviços do Banco.""",
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
        resposta_text = response.text.encode('utf-8').decode('utf-8')
        history.append({"role":"user","parts":[mensagem]})
        history.append({"role":"model","parts":[resposta_text]})
        return jsonify({'resposta': resposta_text}), 200
    else:
        return jsonify({'erro': 'Mensagem não fornecida'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
