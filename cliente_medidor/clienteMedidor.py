#Lara Esquivel de Brito Santos

import socket
import json 
import time,schedule
import random
import threading

class Cliente_Medidor:
    '''
    Classe responsável pelas operações do lado do cliente no medidor
    '''

    def __init__(self,id,cpf,host="localhost",port=8080):
        '''
        Arguments
        id - Int : Identificador do medidor
        cpf - Int : Identificador do usuário
        host - String : Diretório
        port - Int : Porta
        '''
        self.host = host
        self.port = port
        self.id = id
        self.id_cliente = cpf
        self.medidor_cliente_server = None
        self.minutes = 5
        
        
        self.medidor_cliente_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def start(self):
        '''
        Thread responsável por agendamento das chamadas automáticas do medidor
        '''
        schedule.every(self.minutes).minutes.do(self.post_fast_consumo)

        t = threading.Thread(target=self.run_schedule)
        t.start()

    def run_schedule(self):
            '''
            Chama todas os agendamentos pendentes
            '''
            schedule.run_pending()
            time.sleep(1)

#    def connect(self):
#        self.medidor_cliente_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#        self.medidor_cliente_server.connect((self.host,self.port))
            
    def send(self,request):
        '''
        Envia os dados'''
        self.medidor_cliente_server.sendto(request.encode(),(self.host,self.port))

    def recive(self):
        '''
        Recebe os ddos

        Returns:
        msg - Mensagem recebida
        '''
        dados, addr = self.medidor_cliente_server.recvfrom(1024)
        msg = dados.decode()
        print(msg)
        return msg
    
    def post_consumo(self,value,timestamp):
        '''
        Publica o consumo de forma manual

        Arguments:
        value - Valor da medição
        timestamp - Float : Timestamp
        '''
        if self.medidor_cliente_server is not None:
            #json_string = {"id": self.id_cliente, "id_medidor": self.id,"valor":value,"timestamp":time.time()}
            #json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
            #size =len(json_string)
            #request = f'POST /postConsumo HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
            request = f'{self.id_cliente},{self.id},{value},{timestamp}'
            return request
    
    
    def post_fast_consumo(self):
        '''
        Publica o consumo de forma automática
        
        '''
        value = random.triangular(0,300,10)
        request = f'{self.id_cliente},{self.id},{value},{time.time()}'
        #json_string = {"id": self.id_cliente, "id_medidor": self.id,"valor":value,"timestamp":time.time()}
        #request = json.dumps(json_string,separators=(',',':'),indent='\t')
        #size =len(json_string)
        #request = f'POST /postConsumo HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        try:
            self.send(request)
            #reponse = self.recive()
            
        except socket.error as e:
            print(e)
            time.sleep(5)
        


