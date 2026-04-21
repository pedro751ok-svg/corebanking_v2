from flask import Blueprint , jsonify , request
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conta import Conta

client_transacao_bp = Blueprint("cliente_transacao", __name__)

@client_transacao_bp.route('/cliente/<cpf>', methods=['POST'])
def transacoes_deposito(cpf):
    dados = request.json
    valor_num = dados.get('valor')
    conta = Conta.carregar_conta(cpf)

    if not conta:
        return jsonify({"ERRO:""conta nao encontrada"}),404
    
    if conta.depositar(valor_num):
      

        return jsonify({
                "mensagem": 'deposito realizado',
                "cpf":cpf,
                "saldo atual":conta.saldo
                }),200
    
    return jsonify({"erro","falaha ao depositar"}),500

