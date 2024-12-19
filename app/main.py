from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mensagem', methods=['POST'])
def responder_mensagem():
    mensagem = request.json.get('mensagem')
    if mensagem:
        return jsonify({'resposta': f'{mensagem} RECEBIDA'})
    else:
        return jsonify({'erro': 'Mensagem não fornecida'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
