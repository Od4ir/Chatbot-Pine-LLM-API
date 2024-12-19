from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

def get_quote_currency(moeda_requerida:str, moeda_base:str):
    """
    Args: 
        moeda_requirida: Moeda para qual deseja saber o câmbio
        moeda_base: Moeda usada como comparação com a moeda requirida
    return:
        response.json() (dict): dicionario com varias informações a cotação da moeda requirida em relação a moeda base
    """
    response = requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda_requerida}-{moeda_base}")
    return response.json()

def transfer_to_human():
    """
    Args:
    return: 
        recado (string): recado de transferencia para um atendente humano
    """
    recado = "Deve transferir para um atendente humano"
    return recado

tool = [get_quote_currency, transfer_to_human]

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
    system_instruction="Seu nome é Agente Pinho e você é um assistente virtual do Banco Pine. Suas tarefas é responder os clientes de forma mais amigavel possível e conseguir resolver questões bancárias dos clientes do banco como consulta de saldo de conta, gerar os extratos bancários, informar sobre investimentos e sobre o mercado financeiro. Você não deve responder questões fora dos assuntos de mercado financeiro, transações ou serviços do Banco.",
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
