import os
from flask import Flask, render_template_string, request, redirect, url_for, flash
from dotenv import load_dotenv
from together import Together
import smtplib
from email.message import EmailMessage

# Carrega variáveis de ambiente
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

client = Together(api_key=TOGETHER_API_KEY)

def obter_resposta_ia(prompt):
    resposta = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.choices[0].message.content.strip()

def enviar_email(destinatario, assunto, corpo):
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL
    msg['To'] = destinatario
    msg.set_content(corpo)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

app = Flask(__name__)
app.secret_key = 'segredo'  # Necessário para flash messages

HTML_FORM = """
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Assistente de E-mail IA</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      background: #f4f6fb;
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 520px;
      margin: 40px auto;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 24px #0001;
      padding: 32px 28px 24px 28px;
    }
    h2 {
      color: #2d3a4a;
      text-align: center;
      margin-bottom: 24px;
    }
    label {
      font-weight: 500;
      color: #2d3a4a;
    }
    textarea, input[type="text"], input[type="email"] {
      width: 100%;
      padding: 10px;
      margin: 8px 0 16px 0;
      border: 1px solid #cfd8dc;
      border-radius: 6px;
      font-size: 1rem;
      resize: vertical;
      box-sizing: border-box;
    }
    input[type="submit"] {
      background: #4f8cff;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 12px 0;
      width: 100%;
      font-size: 1.1rem;
      font-weight: bold;
      cursor: pointer;
      transition: background 0.2s;
    }
    input[type="submit"]:hover {
      background: #2563eb;
    }
    .msg {
      margin: 18px 0 0 0;
      padding: 12px;
      border-radius: 6px;
      background: #e3fcec;
      color: #256029;
      border: 1px solid #b7ebc6;
      font-size: 1rem;
    }
    .msg.error {
      background: #ffeaea;
      color: #a94442;
      border: 1px solid #f5c6cb;
    }
    ul {
      padding-left: 18px;
    }
    @media (max-width: 600px) {
      .container {
        padding: 16px 6px 12px 6px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Assistente de E-mail IA</h2>
    <form method=post>
      <label>Descreva o conteúdo do e-mail:</label>
      <textarea name=instrucao rows=4 required>{{ instrucao or '' }}</textarea>
      <input type=submit value="Gerar E-mail">
    </form>
    {% if email %}
      <h3 style="margin-top:32px;">E-mail Gerado:</h3>
      <form method=post action="{{ url_for('enviar') }}">
        <textarea name=corpo rows=10 required>{{ email }}</textarea>
        <label>Destinatário:</label>
        <input name=destinatario type="email" required>
        <label>Assunto:</label>
        <input name=assunto type="text" required>
        <input type=submit value="Enviar E-mail">
      </form>
    {% endif %}
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="msg{% if 'erro' in messages[0]|lower %} error{% endif %}">
          <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
          </ul>
        </div>
      {% endif %}
    {% endwith %}
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    email = None
    instrucao = ''
    if request.method == 'POST':
        instrucao = request.form['instrucao']
        prompt = f"Escreva um e-mail profissional com base na seguinte instrução: {instrucao}"
        email = obter_resposta_ia(prompt)
    return render_template_string(HTML_FORM, email=email, instrucao=instrucao)

@app.route('/enviar', methods=['POST'])
def enviar():
    corpo = request.form['corpo']
    destinatario = request.form['destinatario']
    assunto = request.form['assunto']
    try:
        enviar_email(destinatario, assunto, corpo)
        flash('E-mail enviado com sucesso!')
    except Exception as e:
        flash(f'Erro ao enviar e-mail: {e}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)