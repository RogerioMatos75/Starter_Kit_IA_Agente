import os
import json
import io
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import stripe

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a chave secreta do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Inicializa a aplicação Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) # Adiciona suporte a CORS para todas as rotas

# --- ROTAS DA LANDING PAGE E PAGAMENTO ---

@app.route('/')
def index():
    """Serve a página de apresentação (landing.html)."""
    return render_template('landing.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Cria uma sessão de checkout no Stripe."""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'E-mail é obrigatório'}), 400

    try:
        # Preço do Plano Starter (em centavos)
        # R$ 44,50 = 4450 centavos
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'boleto'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': 'Archon AI - Plano Starter',
                            'images': [url_for('static', filename='assets/5logo_Archon.png', _external=True)],
                        },
                        'unit_amount': 4450,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
            customer_email=email,
            metadata={
                'github_repo': os.getenv('GITHUB_REPO_URL') # URL do repositório a ser enviado
            }
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        print(f"[ERRO STRIPE] {e}")
        return jsonify(error=str(e)), 500

@app.route('/success')
def success():
    """Página de sucesso após o pagamento."""
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    """Página de cancelamento do pagamento."""
    return render_template('cancel.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint que recebe notificações (webhooks) do Stripe.
    Verifica a assinatura do evento e, em caso de pagamento bem-sucedido,
    dispara a lógica de envio de e-mail.
    """
    event = None
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    if not webhook_secret:
        print("[ERRO WEBHOOK] A variável de ambiente STRIPE_WEBHOOK_SECRET não está configurada.")
        return jsonify(error="Configuração de servidor incompleta"), 500

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Payload inválido
        return jsonify(error=str(e)), 400
    except stripe.error.SignatureVerificationError as e:
        # Assinatura inválida
        print(f"[ERRO WEBHOOK] Falha na verificação da assinatura: {e}")
        return jsonify(error=str(e)), 400

    # Lida com o evento de checkout bem-sucedido
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        repo_url = session['metadata'].get('github_repo', 'URL_DO_REPO_NAO_CONFIGURADA')
        print(f"[SUCESSO PAGAMENTO] Pagamento recebido de: {customer_email}")
        print(f"-> [AÇÃO] Enviando e-mail com o link do repositório: {repo_url} para {customer_email}")
        # TODO: Implementar a lógica de envio de e-mail aqui.
        # Ex: send_repo_link_email(customer_email, repo_url)

    return jsonify(success=True), 200

if __name__ == '__main__':
    # Este bloco é para rodar a "loja" (landing page) localmente para testes.
    print("-" * 50)
    print("Iniciando servidor web da LANDING PAGE para DESENVOLVIMENTO LOCAL...")
    print("Acesse http://127.0.0.1:5001 no seu navegador.")
    app.run(debug=True, port=5001)
