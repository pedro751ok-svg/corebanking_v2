from conect import conexao
def registrar_transacoes(conn,conta_id,tipo,valor):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO transacoes (conta_id,tipo,valor)
                VALUES (%s,%s,%s)""",(conta_id,tipo,valor))
            conn.commit()

    except Exception as erro:
        conn.rollback()
        print(f'error ao registrar transação{erro}')