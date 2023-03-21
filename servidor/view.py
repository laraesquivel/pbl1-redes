from cliente import Cliente
import json
import asyncio

clientes = []

def get_home():
    return {'response' : "Hello World!"}

def cad_cliente(id,name):
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
    response = {'cliente':len(clientes)}
    response = json.dumps(response)
    return 'HTTP/1.1 200 Ok\r\nContent-Length: 15\r\n\r\n'+response

def cad_medidor(cliente_id):
    for cli in clientes:
        if cli.id == cliente_id:
            cli.add_new_medidor()
            return 'HTTP/1.1 201 Createad\r\nContent-Length: 12\r\n\r\nCriado'
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 12\r\n\r\nNot Found'
        
def post_consumo(id_cliente,id_medidor,valor,timestamp): #Enviar consumo
    for cli in clientes:
        if cli.id == id_cliente:
            cli.update_value(id_medidor,valor,timestamp)
            return 'HTTP/1.1 201 Atualizado\r\nContent-Length: 15\r\n\r\nCriado'
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 12\r\n\r\nN achei'

def get_fatura(id_cliente): #Gerar fatura 
    for cli in clientes:
        if cli.id == id_cliente:
            fatura = cli.get_fatura()
            response = json.dumps(fatura)
            size = len(response)
            return f'HTTP/1.1 200 Ok\r\nContent-Length: {size}\r\n\r\n'+response
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\n\r\nNot Found'
            

def get_excesso(id_cliente): #Alerta de excesso
    for cli in clientes:
        if cli.id == id_cliente:
            alarme = cli.get_alarme()
            response = json.dumps(alarme)
            size = len(response)
            return f'HTTP/1.1 200 Ok\r\nContent-Length: {size}\r\n\r\n'+response
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\n\r\nNot Client'


def get_consumo_geral(id_cliente,periodo,kind): #pegar o consumo geral
    for cli in clientes:
        if cli.id == id_cliente:
            soma,consumo = cli.get_consumo(kind,periodo)
            response = {'id':id_cliente,'soma':soma,'consumo':consumo}
            response = json.dumps(response)
            size = len(response)
            return f'HTTP/1.1 200 Ok\r\nContent-Length: {size}\r\n\r\n'+response
    return 'HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\n\r\nNot Client'

        

        

