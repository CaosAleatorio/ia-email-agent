import os
import ssl
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from together import Together

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")  # Use App Password, não a senha normal

# Inicializa o cliente da Together AI
client = Together(api_key=TOGETHER_API_KEY)

def obter_resposta_ia(prompt):
    resposta = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.choices[0].message.content.strip()

def enviar_email(destinatario, assunto, corpo):
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = EMAIL
    msg["To"] = destinatario
    msg.set_content(corpo)

    max_retries = 3

    for tentativa in range(1, max_retries + 1):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL, APP_PASSWORD)
                smtp.send_message(msg)
            print(f"E-mail enviado para {destinatario} na tentativa {tentativa}!")
            break
        except (TimeoutError, smtplib.SMTPException) as e:
            print(f"Tentativa {tentativa} falhou: {e}")
            time.sleep(5)
    else:
        print("Não foi possível enviar o e-mail após várias tentativas.")

def compor_e_enviar_email():
    instrucao = input("Descreva o conteúdo do e-mail que deseja compor:\n")
    prompt = f"Escreva um e-mail profissional com base nesta instrução: {instrucao}"
    corpo = obter_resposta_ia(prompt)
    print("\n--- E-mail Composto ---")
    print(corpo)
    if input("\nDeseja enviar este e-mail? (sim/não)\n").strip().lower() in ['sim', 's']:
        dest = input("Endereço do destinatário:\n").strip()
        subj = input("Assunto do e-mail:\n").strip()
        enviar_email(dest, subj, corpo)

def responder_e_enviar_email():
    conteudo = input("Cole o conteúdo do e-mail recebido:\n")
    prompt = f"Escreva uma resposta apropriada para o seguinte e-mail:\n{conteudo}"
    resposta = obter_resposta_ia(prompt)
    print("\n--- Resposta Gerada ---")
    print(resposta)
    if input("\nDeseja enviar esta resposta? (sim/não)\n").strip().lower() in ['sim', 's']:
        dest = input("Endereço do destinatário:\n").strip()
        subj = input("Assunto do e-mail:\n").strip()
        enviar_email(dest, subj, resposta)

def assistente_email():
    print("📧 Assistente de E-mails IA pronto!")
    while True:
        print("\nOpções:")
        print("1 – Compor e enviar um novo e-mail")
        print("2 – Responder e enviar um e-mail")
        print("3 – Sair")
        escolha = input("Escolha (1‑3):\n").strip()
        if escolha == '1':
            compor_e_enviar_email()
        elif escolha == '2':
            responder_e_enviar_email()
        elif escolha == '3':
            print("Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    assistente_email()
