from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        # TODO: somente 10 transações diaria, validar
        transacao
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero ):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo and valor <= 500:
            self._saldo -= valor
            return True  # Retorna True para indicar que o saque foi bem-sucedido
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque = 3, limite_transacao = 10):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saque = limite_saque
        self.limite_transacao = limite_transacao
    
    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__ and transacao["data"].split(" ")[0] == datetime.now().strftime("%d-%m-%Y")]
        )

        numero_transacao = len(
            [transacao for transacao in self.historico.transacoes if transacao["data"].split(" ")[0] == datetime.now().strftime("%d-%m-%Y")]
        )

        excedeu_limite = valor>self.limite
        excedeu_saque = numero_saque >= self.limite_saque
        excedeu_transacao = numero_transacao  >= self.limite_transacao

        if excedeu_limite:
            print("\n==== Falha na operação! ====\n-- Valor de saque ultrapassou o limite. --")
        elif excedeu_saque:
            print("\n==== Falha na operação! ====\n-- Numero de saques ultrapassou o limite. --")
        elif excedeu_transacao:
            print("\n==== Falha na operação! ====\n-- Numero de transacao ultrapassou o limite. --")

        else:
            return super().sacar(valor)
        return False
    
    def depositar(self, valor):

        numero_transacao = len(
            [transacao for transacao in self.historico.transacoes if transacao["data"].split(" ")[0] == datetime.now().strftime("%d-%m-%Y")]
        )

        excedeu_transacao = numero_transacao  >= self.limite_transacao

        if excedeu_transacao:
            print("\n==== Falha na operação! ====\n-- Numero de transacao ultrapassou o limite. --")
        else:
            return super().depositar(valor)
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Tirular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            }
        )
    
    # TODO: filtar todas as transações do dia
    def transacoes_dia(self):
            return [transacao for transacao in self.historico.transacoes if transacao["data"] == datetime.now()]



class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass 


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


###funções
# def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques)
# def deposito(saldo, valor, extrado)
# def extrato(saldo, *, extrato)
# def cria_usuario()
# def cria_conta()
# def lista_usuario()
# def lista_conta()
# def lista_conta_usuario(cpf_usuario)
# def tranferencia(conta_saida, conta_entrada, saldo, valor, extrato, limite)


def menu_principal():
    menu = """
        #####MENU#####
        [1] Acessar Conta
        [2] Cadastar Usuario
        [3] Criar Conta
        [4] Listar Usuarios
        [5] Listar Contas de Usuario
        [0] Sair
            
        ==> """
    return input(textwrap.dedent(menu))


def menu_cliente():
    menu = """
        #####MENU#####
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Saldo
        [0] Sair
            
        ==> """
    return input(textwrap.dedent(menu))

def verifica_usuario(clientes, cpf):
    for usuario in clientes:
        if cpf == usuario.cpf:
            return usuario  
    return None


def acessar_conta(clientes):
    cpf = input('CPF: ')
    cliente = verifica_usuario(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    if not cliente.contas:
        print("Cliente não possui conta")
        return
    
    while True:
        opcao = menu_cliente()

        if opcao.isdigit():  # Check if input is a digit (number)
            match int(opcao):
                case 1:
                    valor_deposito = float(input("valor do depósito: R$"))
                    depositar(cliente, valor_deposito)

                case 2:
                    valor = float(input("valor do depósito: R$"))
                    sacar(cliente, valor)

                case 3:
                    extrato(cliente)

                case 4:
                    saldo(cliente)

                case 0:
                    break

                case default:
                    print("Opcao invalida!")
        else:
            print("Valor inválido. Digite um número.")

        



def cadastrar_usuario(clientes):
    print('###Cadastro de novo Usuario')
    nome = input('Nome: ')
    data_nascimento = input('Data de nascimento: ')
    cpf = input('CPF: ')
    endereco = input('Endereco: ')

    cliente = verifica_usuario(clientes, cpf)

    if cliente:
        print("Cliente já cadastrado")
        return
    
    cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    

def criar_conta(clientes, contas, numero_conta):
    print('###Cadastro de novo Usuario')
    cpf = input('CPF: ')

    cliente = verifica_usuario(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)


def listar_usuarios(clientes):
    print("====Listra de Clientes====")
    for usuario in clientes:
        print(f'{usuario.nome} - {usuario.cpf}')


def listar_contas_cliente(clientes, contas):
    cpf = input('CPF: ')

    cliente = verifica_usuario(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    print("====Listra de Contas por Cliente====")
    for conta in cliente.contas:
        print(textwrap.dedent(str(conta)))



def depositar(cliente, valor):
    transacao = Deposito(valor)
    cliente.realizar_transacao(cliente.contas[0], transacao)


def sacar(cliente, valor):
    transacao = Saque(valor)
    cliente.realizar_transacao(cliente.contas[0], transacao)


def extrato(cliente):
    extrato = cliente.contas[0].historico.transacoes
    print(" EXTRATO ".center(54,'='))
    if not extrato:
        print("Sem transações.")
    else:
        for transacao in extrato:
            print((f'{transacao["tipo"]}:').ljust(20),f'R$ {transacao["valor"]:<10.2f} {transacao["data"]}')
    print("".center(54,'='))
    print(('Saldo:').ljust(20), f'R$ {cliente.contas[0].saldo:.2f}')
    print("".center(54,'='))


def saldo(cliente):
    print(('Saldo:').ljust(15), f'R$ {cliente.contas[0].saldo:.2f}')

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu_principal()
        if opcao.isdigit():  # Check if input is a digit (number)
            match int(opcao):
                case 1:
                    acessar_conta(clientes)
                case 2:
                    cadastrar_usuario(clientes)
                case 3:
                    numero_conta = len(contas) + 1
                    criar_conta(clientes, contas, numero_conta)
                case 4:
                    listar_usuarios(clientes)
                case 5:
                    listar_contas_cliente(clientes, contas)
                case 0:
                    break
                case default:
                    print("Opcao invalida!")
        else:
            print("Valor inválido. Digite um número.")

        


if __name__ == "__main__":
    main()