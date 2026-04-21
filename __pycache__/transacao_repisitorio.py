class TransacaoRepository:
    def __init__(self, conn):
        self.conn = conn

    def contar_por_tipo_e_conta(self, conta_id, tipo):
        with self.conn.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                FROM transacoes
                WHERE conta_id = %s AND tipo = %s
            """, (conta_id, tipo))
            return cursor.fetchone()[0]