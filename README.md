Prime Bank - Sistema de Core Banking
Este projeto consiste em um sistema de backend para operações bancárias estruturado em Python. O software integra a lógica de gerenciamento de contas, processamento de transações e uma camada de serviços via API REST com Flask, incluindo um módulo para análise comportamental de usuários.

Arquitetura do Sistema
O repositório está organizado para separar a lógica de domínio da camada de interface:

1. Núcleo de Processamento (Core)
Localizado na raiz do projeto, este módulo contém a inteligência de negócios:

Gerenciamento de Entidades: Definições de clientes e contas nos arquivos Clientes.py e Conta.py.

Fluxo Financeiro: Processamento de depósitos, saques e transferências através de transacoes.py e transacao_repositorio.py.

Persistência e Conectividade: Módulo conect.py responsável pela integração com a base de dados.

2. Camada de API (Flask)
A pasta api_flask centraliza os serviços de comunicação externa, permitindo que sistemas front-end ou outros microserviços interajam com o core banking:

api.py: Ponto de entrada do serviço Flask.

Módulos de Rota: Separação de responsabilidades para cadastro de clientes, postagens e operações financeiras (cliente_rout.py, saque_deposito_rout.py, etc).

3. Análise de Dados (ML)
O módulo ml.py implementa uma lógica de análise para classificação automática de nível de conta. O sistema avalia métricas de uso para determinar o tiering do cliente, permitindo a aplicação de regras de negócio dinâmicas com base no perfil identificado.

Tecnologias Utilizadas
Linguagem: Python 3.10+

Framework Web: Flask

Ambiente: Suporte a variáveis de ambiente via .env

Arquitetura: Programação Orientada a Objetos (POO) com separação em camadas

Instruções de Instalação e Uso
Pré-requisitos
Python instalado

Gerenciador de pacotes pip

Configuração
Clone o repositório.

Instale as dependências:

Bash
pip install flask python-dotenv
Configure o arquivo .env com as credenciais necessárias.

Execução
Para iniciar o servidor da API:

Bash
python api_flask/api.py
Para executar o fluxo principal do sistema:

Bash
python main.py
Status do Projeto
O sistema encontra-se em fase de expansão de funcionalidades, com foco em segurança de transações e escalabilidade das rotas de API.
