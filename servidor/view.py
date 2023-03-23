#Este módulo foi feito por Lara Esquivel de Brito Santos

from cliente import Cliente
import json
import asyncio

clientes = []

#Retorna home
def get_home():
    return {'response' : "Hello World!"}

#Responsável por cadastrar cliente
def cad_cliente(id,name):
    '''
    Arguments:

    id - Int: Identificador do usuario
    name - String: Nome do usuário

    Returns;

    String -> Resposta HTPP informando o estado da solicitação feita: Cliente já está cadastrado ou Criado
    '''
    cliente = Cliente(id,name)
    if cliente.id == 0:
        response = {'errors:':'Cliente já está cadastrado!'}
        response = json.dumps(response)
        size = len(response)
        return f'HTTP/1.1 409 Conflict\r\nContent-Length: {size}\r\n\r\n'+response
    else:
        clientes.append(cliente)
        return 'HTTP/1.1 201 Createad\r\nContent-Length: 12\r\n\r\nCriado'


def get_clientes():
    '''
    Retorna o numero de clientes cadastrados
    '''
    response = {'cliente':len(clientes)}
    response = json.dumps(response)
    return 'HTTP/1.1 200 Ok\r\nContent-Length: 15\r\n\r\n'+response

def cad_medidor(cliente_id):
    '''
    Cadastrar medidor
    Arg:
    cliente_id -> Int: Identificador do cliente

    Returns: String - Mensagem http com o estado: Criado ou não encontrado
    '''
    for cli in clientes:
        if cli.id == cliente_id:
            cli.add_new_medidor()
            return 'HTTP/1.1 201 Createad\r\nContent-Length: 12\r\n\r\nCriado'
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 12\r\n\r\nNot Found'
        
def post_consumo(id_cliente,id_medidor,valor,timestamp): #Enviar consumo
    '''
    Recebe consumo do usuário
    id_cliente -> Int : Identificador do cliente
    id_medidor -> Int : Identificador do medidor

    valor -> Float : valor da medição
    timestamp - Number (Float ou Int) : Timestamp referente a medição
    '''
    for cli in clientes:
        if cli.id == id_cliente:
            cli.update_value(id_medidor,valor,timestamp)
            return 'HTTP/1.1 201 Atualizado\r\nContent-Length: 15\r\n\r\nCriado'
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 12\r\n\r\nN achei'

def get_fatura(id_cliente): #Gerar fatura 
    '''
    Dado um id, calcula e retorna a fatura do cliente, com uma resposta codifica com a fatura ou a mensagem de não encontrado
    '''
    for cli in clientes:
        if cli.id == id_cliente:
            fatura = cli.get_fatura()
            response = json.dumps(fatura)
            size = len(response)
            return f'HTTP/1.1 200 Ok\r\nContent-Length: {size}\r\n\r\n'+response
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\n\r\nNot Found'
            

def get_excesso(id_cliente): #Alerta de excesso
    '''
    Dado um Id emite um uma  mensagem de verificação para a chamada do alarme
    '''
    for cli in clientes:
        if cli.id == id_cliente:
            alarme = cli.get_alarme()
            response = json.dumps(alarme)
            size = len(response)
            return f'HTTP/1.1 200 Ok\r\nContent-Length: {size}\r\n\r\n'+response
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\n\r\nNot Client'


def get_consumo_geral(id_cliente,periodo,kind): #pegar o consumo geral
    '''
    Dado um id de um cliente, o perido e um tipo de periodo, este retorna o histórico de consumo de um cliente
    '''
    for cli in clientes:
        if cli.id == id_cliente:
            soma,consumo = cli.get_consumo(kind,periodo)
            response = {'id':id_cliente,'soma':soma,'consumo':consumo}
            response = json.dumps(response)
            size = len(response)
            return f'HTTP/1.1 200 Ok\r\nContent-Length: {size}\r\n\r\n'+response
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\n\r\nNot Client'

        

        

