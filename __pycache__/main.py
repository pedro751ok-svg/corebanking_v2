from conect import conexao
from clientes import Cliente
from conta import Conta
from transacao_repisitorio import TransacaoRepository
from ml import modelo, extrair_dados_da_conta, prever_nivel
from decimal import Decimal
# ============================ MENU TRANSAÇÃO ============================
def menu_transacao(conexao_banco, objeto_conta):
    if objeto_conta is None:
        print("Faça login primeiro")
        return

    
    meu_repo = TransacaoRepository(conexao_banco)

    while True:
        print("\n1 - Ver saques | 2 - Ver depósitos | 0 - Voltar")
        escolha = input("Escolha: ")

        if escolha == "1":
            
            qtd = meu_repo.contar_por_tipo_e_conta(objeto_conta.id, "saque")
            print(f"Saques: {qtd}")

        elif escolha == "2":
            qtd = meu_repo.contar_por_tipo_e_conta(objeto_conta.id, "deposito")
            print(f"Depósitos: {qtd}")

        elif escolha == "0":
            break

def menu():
    cliente = None
    conta = None
    conn = conexao()

    try:
        while True:
            print('\n1-Cadastrar | 2-Login | 3-Depositar | 4-Sacar | 5-Saldo | 6-Transações | 0-Sair')
            opcao = input('Opção: ')

            if opcao == '0': break
            elif opcao == '1': cadastrar(conn)
            elif opcao == '2':
                resultado = login(conn)
                if resultado: cliente, conta = resultado
                if conta is not None:
                    try:               
                            dados = extrair_dados_da_conta(conta, conn) 
                            nivel_num = prever_nivel(modelo, dados)    
                            print(f'\nBem-vindo, {cliente.nome}!')                       
                            print(f'Nível da conta: {nivel_num}')
                    except Exception as erro:
                            conn.rollback()
                            print(f"Erro ao calcular nível: {erro}")
            elif opcao == '3': depositar(conta, conn)
            elif opcao == '4': saque(conta, conn)
            elif opcao == '5': ver_saldo(conta, conn)
            elif opcao == '6': menu_transacao(conn, conta) 
            else:
                print("Opção inválida!") 

    except Exception as erro:
        print(f'Erro no menu: {erro}')
    finally:
        conn.close()
# ============================ CADASTRAR =================================
def cadastrar(conn):
    print('\n--- MENU DE CADASTRO ---')
    try:
        with conn.cursor() as cursor:
            nome = input('Nome: ')
            cpf = input('CPF: ')
            email = input('Email: ')
            senha = input('Senha: ')

            novo_cliente = Cliente(nome, cpf, email, senha)

            if not novo_cliente.cpf_validado(cpf):
                print('CPF inválido!')
                return

            cursor.execute("""
                INSERT INTO clientes(nome, cpf, email, senha)
                VALUES(%s, %s, %s, %s) RETURNING id
            """, (novo_cliente.nome, novo_cliente.cpf, novo_cliente.email, novo_cliente.senha_hash))

            cliente_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO contas(cliente_id, saldo, limite)
                VALUES(%s, %s, %s)
            """, (cliente_id, 0.0, 200.0))

            conn.commit()
            print("Cadastrado com sucesso!")
    except Exception as erro:
        conn.rollback()
        print(f'Erro no cadastro: {erro}')

# ============================ LOGIN =====================================
def login(conn):
    print('\n--- MENU DE LOGIN ---')
    try:
        cpf = input('CPF: ')
        senha = input('Senha: ')

        cliente = Cliente.carregar_por_cpf(cpf)
        if not cliente or not cliente.validar_senha(senha):
            print('Credenciais incorretas.')
            return None

        conta = Conta.carregar_conta(cpf)
        
        if not conta:
            print('Conta não encontrada.')
            return None

        print('Login concluído!')
        return cliente, conta
    except Exception as erro:
        print(f'Erro no login: {erro}')
        return None

# ============================ OPERAÇÕES =================================
def depositar(conta, conn):
    if conta is None:
        print('Faça login primeiro.')
        return
    try:
        valor = Decimal(input('Valor: '))
        conta.depositar(valor, conn)
    except Exception as erro:
        conn.rollback()
        print(f'Erro: {erro}')

def saque(conta, conn):
    if conta is None:
        print('Faça login primeiro.')
        return
    try:
        valor = Decimal(input('Valor: '))
        conta.sacar(valor, conn)
    except Exception as erro:
        conn.rollback()
        print(f'Erro: {erro}')

def ver_saldo(conta, conn):
    if conta is None:
        print('Faça login primeiro.')
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT saldo FROM contas WHERE cliente_id = %s", (conta.cliente_id,))
            resultado = cursor.fetchone()
            if resultado:
                print(f'Saldo: R$ {resultado[0]}')
    except Exception as erro:
        print(f'Erro: {erro}')
menu()