from conect import conexao
from transacoes import registrar_transacoes
#================================================================ CLASS CONTA ============================================================
class Conta:
    def __init__(self,id,cliente_id,saldo,limite):
        self.id = id 
        self.cliente_id = cliente_id
        self.saldo = saldo 
        self.limite = limite
#=============================================INFORMAÇÕES PARA A API=======================================
    def to_dict(self):
        return {
            "id cliente": self.cliente_id,
            "saldo": self.saldo,
            "limite":self.limite
        }
#=============================================== METODO DEPOSITAR CONECTADO DIRETAMENTE COM O BANCO ==================================
    def depositar(self, valor, conn):
        if valor <= 0:
            print('valor invalido')
            return False 

        try:
            with conn.cursor() as cursor:
                
                self.saldo += valor
                
                
                registrar_transacoes(conn, self.id, 'deposito', valor)
                
                
                cursor.execute("""UPDATE contas SET saldo = %s WHERE id = %s""",
                               (self.saldo, self.id))
                
                conn.commit()
                print('deposito realizado com sucesso')
                return True 
                
        except Exception as e:
            conn.rollback()
            print('Erro ao depositar:', e)
            return False  
 #=============================================== METODO SACAR CONECTADO DIRETAMENTE COM O BANCO =======================================
    def sacar(self, valor, conn):
        if valor <= 0:
            print('Valor inválido para saque')
            return False

        if self.saldo + self.limite < valor:
            print('Saldo insuficiente (considerando limite)')
            return False
        try: 
            with conn.cursor() as cursor:
                 
                registrar_transacoes(conn, self.id, 'saque', valor)
                           
                self.saldo -= valor
                             
                cursor.execute("""UPDATE contas SET saldo = %s WHERE id = %s""",
                               (self.saldo, self.id))
                           
                conn.commit()
                print('Saque realizado com sucesso')
                return True 
                
        except Exception as e:
            conn.rollback() 
            print(f'Erro no saque: {e}')
            return False
#============================================ METODO ATUALIZAR SALDO CONECTADO DIRETAMENTE COM O BANCO ===================================
    def atualizar_saldo(self,conn):
        try:    
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE contas SET saldo = %s WHERE cliente_id = %s""",
                    (self.saldo,self.cliente_id))
                conn.commit()
        except Exception as erro:
            conn.rollback()
            print(f'erro ao atualizar saldo{erro}')
#============================================================ METODO CARREGAR CONTA ======================================================
#metodo funcina exectuando um join entre as duas tabelas  contas e clientes,
# retornando dados e buscando pelo cpf do usuario.
    @classmethod
    def carregar_conta(cls,cpf):
        cpf_limpo = str(cpf).strip()
        try:
            with conexao() as conn:
                with conn.cursor() as cursor:
            
                    cursor.execute("""
                       SELECT co.id, co.cliente_id, co.saldo, co.limite 
                        FROM contas co
                        JOIN clientes cl ON co.cliente_id = cl.id
                        WHERE cl.cpf = %s
                    """, (cpf_limpo,))
            
                    dados = cursor.fetchone()
                    if dados:
                
                        return Conta(id=dados[0], cliente_id=dados[1], saldo=dados[2], limite=dados[3])
                    return None
        except Exception as e:
            print(f"Erro ao carregar conta: {e}")
            return None
#====================================== METODO PARA USAR NO ARQUIVO ML, USADO PARA COLETAR INFORMAÇÕES ======================================
    def obter_qtde_saques(self, repo):
        return repo.contar_por_tipo_e_conta(self.id, 'saque')


#====================================== METODO PARA USAR NO ARQUIVO ML, USADO PARA COLETAR INFORMAÇÕES ======================================

    def obter_qtde_depositos(self, repo):
        return repo.contar_por_tipo_e_conta(self.id, 'deposito')
