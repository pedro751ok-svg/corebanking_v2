from flask import Flask
from cliente_rout import cliente_get_bp
from transações_rout import client_transacao_bp
from post_rout import cliente_post_bp
from saque_deposito_rout import cleinte_transacao_rout_bp
app = Flask(__name__)

app.register_blueprint(cliente_get_bp)
app.register_blueprint(cliente_post_bp)
app.register_blueprint(client_transacao_bp)
app.register_blueprint(cleinte_transacao_rout_bp)
if __name__ == '__main__':
    app.run(debug=True)