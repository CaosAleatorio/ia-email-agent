# IA Email Agent

Este projeto é um assistente de e-mails inteligente que utiliza inteligência artificial (IA) para compor, responder, resumir e ajustar o tom de e-mails automaticamente. O usuário interage via terminal ou interface web, descreve o que deseja, e a IA gera o texto do e-mail pronto para envio. O envio é feito utilizando uma conta Gmail, de forma segura, com senha de aplicativo.

**Funcionalidades:**
- Compor e-mails profissionais com IA
- Responder e-mails automaticamente
- Resumir conversas ou e-mails longos
- Ajustar o tom do e-mail (formal/informal)
- Envio seguro via Gmail

**Tecnologias utilizadas:**
- Python 3
- Together AI (API de IA)
- Flask (para interface web)
- smtplib (envio de e-mails)
- python-dotenv (variáveis de ambiente)

**Atenção:**  
Nunca compartilhe seu arquivo `.env` com credenciais. Use o arquivo `.env.example` como modelo.

## Como rodar
1. Instale as dependências com `pip install -r requirements.txt`
2. Configure o arquivo `.env` com suas credenciais
3. Execute o projeto com `python agente.py` ou `python app.py`
