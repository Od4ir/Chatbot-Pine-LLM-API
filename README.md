# Chatbot-Pine-LLM-API
# API Agente Pinho - Assistente Virtual Banco Pine

Esta API é um assistente virtual para o Banco Pine, alimentado pelo modelo de IA do Google, com integração para realizar consultas financeiras e fornecer respostas personalizadas aos clientes. Ela também está configurada para conversar com os clientes de forma amigável e prática.

## Funcionalidades

- **Consulta de câmbio**: O assistente pode buscar a cotação de uma moeda em relação a outra.
- **Transferência para atendente humano**: Caso o assistente não consiga responder, ele orienta a transferência para um atendente humano.
- **Conversa contínua**: O histórico de conversas com o assistente é mantido para um atendimento mais fluído.

## Tecnologias Utilizadas

- **Flask**: Framework web para construção da API.
- **Google Generative AI**: Modelo de linguagem para gerar as respostas personalizadas.
- **Docker**: Para containerizar a aplicação e garantir que ela rode em qualquer ambiente.
- **Docker Compose**: Para orquestrar os serviços e facilitar o setup local.

## Como Rodar Localmente

Para rodar a API localmente, siga os passos abaixo:

### 1. Clonar o repositório

Clone o repositório para sua máquina local:

```bash
git clone https://link-para-o-repositorio.git
cd nome-do-repositorio
```

### 2. Criar e rodar os containers com Docker Compose

Com o Docker e Docker Compose instalados, basta rodar o seguinte comando para subir a API:

```bash
docker-compose up --build
```

Isso irá construir e rodar o serviço Flask dentro de um container Docker, disponível em `http://localhost:5000`.

### 3. Testando a API

Você pode testar a API com o `curl` ou via Postman. Para enviar uma mensagem para o assistente, use o seguinte comando `curl`:

```bash
curl -X POST http://localhost:5000/mensagem -H "Content-Type: application/json" -d '{"mensagem": "Olá, Agente Pinho! Como está o câmbio?"}'
```

O retorno será algo como:

```json
{
  "resposta": "Olá! Tudo bem e você?

Para te ajudar com a cotação do câmbio, preciso de algumas informações. Qual moeda você deseja consultar e em relação a qual moeda base? (ex: Dolar em relação ao Real, Euro em relação ao Real)"
}
```

### 4. Parar os containers

Para parar os containers, basta rodar:

```bash
docker-compose down
```

## Estrutura do Projeto

```plaintext
.
├── app/
│   ├── main.py               # Arquivo principal com a lógica da API
│   ├── requirements.txt      # Dependências do projeto
│   └── Dockerfile            # Dockerfile para containerizar a aplicação
├── docker-compose.yml        # Arquivo de configuração do Docker Compose
└── README.md                 # Este arquivo
```

## Dependências

Para rodar a aplicação, as seguintes dependências são necessárias:

- **Flask**: Framework web para construir APIs em Python.
- **google-generativeai**: Biblioteca para acessar o modelo de IA do Google.

Você pode instalar essas dependências localmente com:

```bash
pip install -r app/requirements.txt
```

## Contribuições

Contribuições são bem-vindas! Se você quiser adicionar novas funcionalidades ou corrigir problemas, sinta-se à vontade para abrir uma **issue** ou enviar um **pull request**.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).