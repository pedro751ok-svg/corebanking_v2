from flask import jsonify, Blueprint
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clientes import Cliente

cliente_get_bp = Blueprint('cliente_get', __name__)

@cliente_get_bp.route('/cliente/<cpf>', methods=['GET'])
def buscar(cpf):

    cliente = Cliente.carregar_por_cpf(cpf)

    if not cliente:
       
        return jsonify({"erro": "cliente nao encontrado"}), 404
    
 
    return jsonify(cliente.to_dict()), 200