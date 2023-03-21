from clienteMedidor import Cliente_Medidor
import threading
import datetime
'''
medidor = Cliente_Medidor(12342)
medidor.connect()

request = 'GET / HTTP/1.1\r\nHost: localhost:8000\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: 33\r\n\r\n{\n\t"word":"ola",\n\t"name":"Lara"\n}'
medidor.send(request)
medidor.recive()
'''

def transform():
     d = input("Insira o dia do consumo")
     m = input("Insira o mês do consumo")
     y = input("Insiria o ano do consumo")
     h = input("Insira a hora do consumo")
     min = input("Insira os minutos do consumo")
     f_string = f"{y}-{m}-{d} {h}:{m}"
     data_hora = datetime.datetime.strptime(f_string, '%Y-%m-%d %H:%M')
     timestamp = datetime.datetime.timestamp(data_hora)
     return timestamp




cpf = input("Insira o cpf do cliente correspondente ao medidor")
medidor_addr = (input("Insira o id do medidor correspondente"))
host = input("Insira o host") 
medidor = Cliente_Medidor(medidor_addr,cpf,host=host)

def interface():
        print(medidor.minutes)
        option = int(input('Insira:\n1:Publicar consumo\n2:Alterar velocidade de envio automático das medições'))
        if option == 1:
            valor = float(input("Insira valor do consumo a publicar"))
            timestap = transform()
            request = medidor.post_consumo(valor,timestap)
            medidor.send(request)
            #msg = medidor.recive()
        elif option == 2:
            time = float(input("Insira a quantidade de tempo em minutos: 1H -> 60 minutos"))
            medidor.minutes = time

while True:
    #medidor.connect()
    #medidor.start()
    interface_t = threading.Thread(target=interface)
    interface_t.start()
    medidor.start()
    interface_t.join()
    


print("Medidor encerrado!")