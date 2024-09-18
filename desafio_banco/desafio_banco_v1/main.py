saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


menu = """
#####MENU#####
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
    
==> """
while True:
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
            
            if valor_saque > limite:
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