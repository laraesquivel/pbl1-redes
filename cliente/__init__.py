#Este módulo foi desenvolvido por Lara Esquivel de Brito Santos

from cliente import Cliente
import threading

def interface_identificao():
    '''
    Função para o identificação do tipo de usuário

    Returns:
    cpf - Identificador do usuário
    lista - Lista com medidores caso seja usuário do tipo cliente
    tipo - O tipo do usuário
    '''
    tipo = input("Digite 1, se vc for servidor público, 2 se você for cliente!")
    while not(tipo == "1" or tipo == "2"):
        tipo = input('Por favor insira um valor válido!')

    cpf = input("Insira o seu cpf!")
    lista =[]
    
    if tipo == "2":
        x=2
        while x:
            val = input("Insira id do medidor que você sabe que possui!")
            lista.append(val)
            x = int(input('Insira 0 se não ter mais medidores a serem adicionados! Caso contrário 1'))
    return(cpf,lista,tipo)

cpf,lista,tipo= interface_identificao()
host = input("Insira o host")
cliente = Cliente(cpf,lista,host=host,minutes=0.5)

def interface():
    '''
    Função responsavel pela interação dos clientes
    '''
    cliente.connect()
    if tipo == "2":
        option = input("Ola! Digite 1 para verificar a sua fatura, 2 para acompanhar a sua conta, e qualquer coisa para encerrar o serviço")
        if option == "2":
            med = int(input("Insira o medidor desejado!"))
            k = input("Insira o tipo periodo que você deseja: D-dias, M-mês, Y-ano").upper()
            periodo = int(input("Insira o número do périodo"))
            request = cliente.get_historico(med,k,periodo)
            cliente.send(request)
            response = cliente.recive()
            print(response)
        elif option == "1":
            request = cliente.get_fatura()
            cliente.send(request)
            response = cliente.recive()
            print(response)
    else:
        option = input("Digite : 1 para cadastrar cliente, 2 para cadastrar medidor")
        if option == '1':
            cpf = input("Insira o cpf do usuário")
            name = input("Insira o nome do usuário")
            request = cliente.cadUser(cpf,name)
            cliente.send(request)
            response = cliente.recive()
            print(response)
        else:
            cpf = input("Insira o cpf do usuario")
            request = cliente.cadMedidor(cpf)
            cliente.send(request)
            response = cliente.recive()
            print(response)

#Execução do programa
#Função interface é passada como alvo da thread interface_t que tem o mais alto grau de prioridade
#Logo o cliente.start() que faz as chamadas dos alarme só será convocada após o termino desta

while True:
    interface_t = threading.Thread(target=interface)
    interface_t.start()
    if tipo == "2":
        cliente.start()
    interface_t.join()
