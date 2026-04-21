from sklearn.tree import DecisionTreeClassifier
from transacao_repisitorio import TransacaoRepository

#classifica nivel de conta,
# usando como referencia ,depositos,saques,saldo,limite,tempo de conta
X = [
    [10,20,1000,300,3],
    [40,10,1500,500,270],
    [60,50,3000,800,15],
    [55,30,2500,600,654],
    [80,90,3000,1000,76],
    [30,22,2500,600,375]
]
Y = [0,0,0,1,1,1]

modelo = DecisionTreeClassifier()
modelo.fit(X,Y)
#========================================= FUNÇÕES QUE FUNCIONAM NO MAIN.PY, POIS RECEBERAO DADOS DO LOGIN ==============================
def extrair_tempo_conta(conn,cliente_id):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT CURRENT_DATE - data_criacao
                       FROM clientes
                       WHERE id =%s""",
                       (cliente_id,))
        resultado = cursor.fetchone()
        return resultado[0].days if resultado else 0

def extrair_dados_da_conta(conta,conn):
    repo = TransacaoRepository(conn)
    return [conta.obter_qtde_saques(repo),
            conta.obter_qtde_depositos(repo),
            float(conta.saldo),
            float(conta.limite),
            extrair_tempo_conta(conn,conta.cliente_id)]

def prever_nivel(modelo,dados_clientes):
    resultado = modelo.predict([dados_clientes])[0]
    return "VIP" if resultado == 1 else "comum"
