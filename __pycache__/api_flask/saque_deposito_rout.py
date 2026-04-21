import os 
import sys
from decimal import Decimal
from conect import conexao
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conta import Conta
from flask import Blueprint, jsonify , request

cleinte_transacao_rout_bp = Blueprint('deposito e saque ', __name__)


@cleinte_transacao_rout_bp.route('/cliente/depositar/<cpf>', methods=['POST'])
def depositar(cpf):
    conn = conexao()
    dados = request.json
    valor = Decimal(dados.get('valor'))
    conta = Conta.carregar_conta(cpf)
    if conta:
        conta.depositar(valor,conn)
        return jsonify({
            "sucesso":"deposito feito com sucesso",
            "saldo atual":float(conta.saldo)
        }),200
    if not conta:
        return jsonify({"erro":"cliente nao encontrado"}),404
@cleinte_transacao_rout_bp.route('/cliente/sacar/<cpf>',methods=['POST'])
def sacar(cpf):
    conn = conexao()
    dados = request.json
    valor = Decimal(dados.get("valor"))
    conta = Conta.carregar_conta(cpf)
    if conta:
        conta.sacar(valor,conn)
        return jsonify({
            "sucesso":"saque realizado com sucesso",
            "saldo atual":float(conta.saldo)
        }),200
    if not conta:
        return jsonify({"erro":"cliente nao encontrado"}),404