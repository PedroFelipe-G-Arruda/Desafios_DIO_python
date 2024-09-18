saldo = 0
extrato = ""
numero_saques = 0
LIMITE = 500
LIMITE_SAQUES = 3

status = False

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

menu = """
#####MENU#####
[1] Acessar Conta
[2] Cadastar Usuario
[3] Criar Conta
[4] Listar Usuarios
[5] Listar Contas de Usuario
[0] Sair
    
==> """

menu_submenu = """
#####MENU#####
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
    
==> """

def saque(*, saldo, valor, extrato, limite, numero_saque, limite_saque):
    if numero_saque == limite_saque:
            print("Limite de saques diários alcançado.")
            return
    else:        
        if valor > limite:
            print("Valor de saque maior que o permitido!")
            
        elif saldo < valor:
            print("Saldo indisponível.")
            
        else:
            texto_saque = 'Saque '.ljust(30, '-') + f' R${valor:.2f}\n'

            extrato += texto_saque
            saldo -= valor
            numero_saque += 1


    return saldo, extrato

def deposito(saldo, valor, extrato):   
    if valor > 0:
        saldo += valor
        texto_deposito = 'Deposito '.ljust(30, '-') + f' R${valor:.2f}\n'
        extrato += texto_deposito
        print(extrato)
    else:
        print('Valor de deposito invalido')
    
    return saldo, extrato

def extrato(saldo, *, extrato):
    print(extrato if extrato else "Nenhuma movimentação realizada.")
    print(f"Saldo total ".ljust(30) +  f" R${saldo:.2f}")
    print("="*50)


def cria_usuario(lista_usuarios):
    print('###Cadastro de novo Usuario')
    nome = input('Nome: ')
    data_nasciemento = input('Data de nascimento: ')
    cpf = input('CPF: ')
    endereco = input('Endereco: ')

    for usuario in lista_usuarios:
        if cpf == usuario['cpf'] :
            print("Usuario já cadastrado")
            return 0
    return {'nome':nome, 'nascimento':data_nasciemento, 'cpf':cpf, 'endereco':endereco}  

def cria_conta(lista_usuarios, numero_conta):
    cpf_usuario = input("Informe o CPF do usuario :")
    
    for index, usuario in enumerate(lista_usuarios):
        if cpf_usuario in usuario.values():
            numero_agencia = '0001' 
            conta = {'agencia': numero_agencia, 'conta':numero_conta, 'saldo': 0, 'limite':500, 'numero_saque':0, 'limite_saque':3, 'extrato': ""}

            if not 'contas' in usuario:
                lista_usuarios[index]['contas'] = []

            lista_usuarios[index]['contas'].append(conta)
           
            numero_conta += 1
        else:
            print('nao tem')

    return lista_usuarios, numero_conta

def lista_usuarios(lista_usuarios):
    for usuario in lista_usuarios:
        print(f'{usuario['cpf']} - {usuario['nome']}')

def lista_conta(lista_usuarios):
    cpf = input('Digite o CPF da conta:')
    for  usuario in lista_usuarios:
        print(usuario)
        if cpf in usuario.values():
            print(f'###{usuario['nome']} - {usuario['cpf']}###')
            for index, contas in enumerate(usuario['contas']):
                print(f'{index} - {contas['agencia']} - {contas['conta']}')

def lista_conta_usuario(cpf_usuario):
    pass

def tranferencia(conta_saida, conta_entrada, saldo, valor, extrato, limite):
    pass

def submenu(usuario):
    while True:
        opcao = int(input(menu_submenu))
        match opcao:
            case 1:
                print("Depósito".center(20,"="))
                valor_deposito = float(input("valor do depósito: R$"))
                usuario['contas'][0]['saldo'], usuario['contas'][0]['extrato'] = deposito(usuario['contas'][0]['saldo'], valor_deposito, usuario['contas'][0]['extrato'])

            case 2:
                print("Saque".center(20,"="))
                valor_saque = float(input("Qual valor deseja sacar: R$"))
                usuario['contas'][0]['saldo'], usuario['contas'][0]['extrato'] = saque(saldo=usuario['contas'][0]['saldo'], valor=valor_saque, extrato=usuario['contas'][0]['extrato'], limite=usuario['contas'][0]['limite'], numero_saque=usuario['contas'][0]['numero_saque'], limite_saque=usuario['contas'][0]['limite_saque'])
                
            case 3:
                print("Saque".center(20,"="))
                extrato(usuario['contas'][0]['saldo'], extrato=usuario['contas'][0]['extrato'])

            case 0:
                break
            case defalt:
                print("Opcao invalida")

    return usuario


def acessar_conta(lista_usuarios):
    cpf = input('CPF: ')
    for index, usuario in enumerate(lista_usuarios):
        if cpf in usuario.values():
            print(index, usuario)
            lista_usuarios[index] =  submenu(usuario)

if __name__ == "__main__":
    print('teste')
    dados_usuarios_contas = [{'nome': 'pedro', 'nascimento': '000', 'cpf': '111', 'endereco': 'gggg', 'contas': [{'agencia': '0001', 'conta': 1, 'saldo': 0,'limite':500, 'numero_saque':0, 'limite_saque':3, 'extrato': ""}]},
                             {'nome': 'mariana', 'nascimento': '001', 'cpf': '222', 'endereco': 'gggg', 'contas': [{'agencia': '0001', 'conta': 2, 'saldo': 0,'limite':500, 'numero_saque':0, 'limite_saque':3, 'extrato': ""}]},
                             {'nome': 'lorena', 'nascimento': '002', 'cpf': '333', 'endereco': 'gggg', 'contas': [{'agencia': '0001', 'conta': 3, 'saldo': 0,'limite':500, 'numero_saque':0, 'limite_saque':3, 'extrato': ""}]}]
    numero_conta = 1
    while True:
        opcao = int(input(menu))

        match opcao:
            case 1:
                acessar_conta(dados_usuarios_contas)
            case 2:
                novo_usuario = cria_usuario(dados_usuarios_contas)
                if novo_usuario:
                    dados_usuarios_contas.append(novo_usuario)
            case 3:
                lista, numero_conta = cria_conta(dados_usuarios_contas, numero_conta)
                if lista:
                    dados_usuarios_contas = lista
            case 4:
                lista_usuarios(dados_usuarios_contas)
            case 5:
                lista_conta(dados_usuarios_contas)
            case 0:
                break
            case defalt:
                print("Opcao invalida")

       


while status:
    opcao = input(menu)
    
    if opcao == "d":
        print("Depósito".center(20,"="))
        valor_deposito = float(input("valor do depósito: R$"))

        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito  - R${valor_deposito:.2f}\n"
        else:
            print("Valor de depósito invalido")
        
    elif opcao  == "s":
        print("Saque".center(20,"="))
        
        if numero_saques == LIMITE_SAQUES:
            print("Limite de saques diários alcançado.")
            
        else:
            valor_saque = float(input("Qual valor deseja sacar: "))
            
            if valor_saque > LIMITE:
                print("Valor de saque maior que o permitido!")
                
            elif saldo < valor_saque:
                print("Saldo indisponível.")
                
            else:
                extrato += f"Saque  - R${valor_saque:.2f}\n"
                saldo -= valor_saque
                numero_saques += 1
        
    elif opcao == "e":
        print("Extrato".center(50,"="))
        print(extrato if extrato else "Nenhuma movimentação realizada.")
        print(f"Saldo total: R${saldo:.2f}")
        print("="*50)
        
    elif opcao == "q":
        break
        
    else:
        print("Opção inválida")