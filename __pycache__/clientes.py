from conect import conexao
import bcrypt


class Cliente:
    def __init__(self, nome, cpf, email, senha, senha_ja_hash=False):
        self.nome = nome
        self.cpf = cpf
        self.email = email

        if senha_ja_hash:
            self.senha_hash = senha 
        else:
            self.senha_hash = bcrypt.hashpw(
                senha.encode(),
                bcrypt.gensalt()
            ).decode('utf-8')

    def validar_senha(self, senha_digitada):
        try:
            return bcrypt.checkpw(
                senha_digitada.encode(),
                self.senha_hash.encode()
            )
        except Exception as erro:
            print(f'erro validar senha: {erro}')
            return False

    # CALCULO CPF
    def calcular_cpf(self, peso):
        soma = 0
        for i in range(peso):
            soma += int(self.cpf[i]) * (peso + 1 - i)
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    # CPF VALIDADO
    @staticmethod  
    def cpf_validado(cpf_para_validar): 
        
        cpf_limpo = ''.join(filter(str.isdigit, str(cpf_para_validar)))

        
        if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
            print('cpf invalido')
            return False

    
        return True

    @classmethod
    def carregar_por_cpf(cls, cpf):
        try:
            with conexao() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT nome, cpf, email, senha
                        FROM clientes
                        WHERE cpf = %s
                    """, (cpf,))

                    dados = cursor.fetchone()

                    if dados:
                        return Cliente(
                            nome=dados[0],
                            cpf=dados[1],
                            email=dados[2],
                            senha=dados[3],
                            senha_ja_hash=True
                        )

                    return None

        except Exception as e:
            conn.rollback()
            print(f"Erro ao buscar cliente: {e}")
            return None 
        
    def salvar(self):
        try:
            
            with conexao() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute("""
                        INSERT INTO clientes (nome, cpf, email, senha)
                        VALUES (%s, %s, %s, %s)
                    """, (self.nome, self.cpf, self.email, self.senha_hash))
                    
                    conn.commit() 
                    return True
        except Exception as e:
            
            print(f"Erro ao salvar no banco: {e}")
            return False
    def to_dict(self):
        return {
        "nome":self.nome,
        "cpf": self.cpf,
        "email":self.email}