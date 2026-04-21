from flask import jsonify, Blueprint, request
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clientes import Cliente
from conect import conexao

cliente_post_bp = Blueprint('cliente_post', __name__)

@cliente_post_bp.route('/cliente/<cpf>', methods=['POST'])
def post_cliente(cpf):
    
    dados_recebidos = request.json
    
    nome = dados_recebidos.get('nome')
    email = dados_recebidos.get('email')
    senha = dados_recebidos.get('senha')

    if not Cliente.cpf_validado(cpf):
        return jsonify({"erro": "CPF falso ou invalido"}), 400

    new_client = Cliente(nome, cpf, email, senha)

    if new_client.salvar():
        try:
            conn = conexao()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO contas(cliente_id, saldo, limite)
                    VALUES(
                        (SELECT id FROM clientes WHERE cpf = %s),
                        0.0,
                        200.0
                    )
                """, (cpf,))
                conn.commit()

            return jsonify({
                "mensagem": "Cliente cadastrado com sucesso",
                "cpf": cpf
            }), 201

        except Exception as erro:
            return jsonify({
                "erro": f"cliente criado, mas erro ao criar conta: {erro}"
            }), 500

    else:
        return jsonify({
            "erro": "Nao foi possivel cadastrar. Verifique se o CPF ja existe."
        }), 400