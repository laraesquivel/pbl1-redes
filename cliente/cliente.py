#Código pertence a Lara Esquivel de Brito Santos

import socket,threading
import json
import schedule,time

class Cliente:
    '''
    Classe dedicada as relações com o cliente em relação a necessidade de conexão com o servidor
    '''
    
    def __init__(self,cpf,medidores,minutes=3,host="localhost",port=8888):
        '''
        Arguments : 
        cpf - String : Cpf é utilizado como identificador de usuários
        medidores - Array: que passa a lista de medidores que o usuário passa
        minutes - Int: Tempo em minutos para chamada 
        host - String: Endereço do host
        port - Int: Porta
        '''
        self.cpf = cpf
        self.medidores = medidores 
        self.host = host
        self.port = port
        self.cliente = None
        self.minutes = minutes
    
    def start(self):
        '''
        Inicia a thread que envia o alarme de forma agendada
        '''
        schedule.every(self.minutes).minutes.do(self.get_alarm)
        t = threading.Thread(target=self.run_schedule)
        t.start()

    def run_schedule(self):
        '''
        Chama todas os agendamentos pendentes para serem executados
        '''
        schedule.run_pending()
        time.sleep(1)
    
    def connect(self):
        '''
        Estabelece conexão com o socket do servidor
        '''
        self.cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cliente.connect((self.host,self.port))

    def send(self,request):
        '''
        Envia as requisições
        Arguments:
        request - Requisição empacotada em formato JSON
        '''
        self.cliente.sendall(request.encode())
    
    def recive(self):
        '''
        Recebe todas as requisições lendo 1024 bytes

        Returns ->
        response - String : String corrrespondente a um json decodificada
        '''
        response = self.cliente.recv(1024)
        response = response.decode()
        return response

    def get_historico(self,medidor_id,kind,periodo):
        '''
        Solicita histórico de medições 

        Arguments:
        medidor_id -> Int: Id do medidor
        kind -> String : String correspondente sobre qual periodo desejado podendo ser: D, M ou Y
        periodo -> Int : Periodo do histórico desejado

        Returns:
        request -> String: String correspondente a um json codificado
        '''
        m = self.medidores[medidor_id-1]
        json_string = {"id":self.cpf,"id_medidor":m,"kind":kind,"periodo":periodo}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'GET /getConsumoHist HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request
    
    def get_alarm(self):
        '''
        Solicita alarme

        '''
        json_string = {"id":self.cpf}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        print("Estou solicitando alarme...")
        request = f'GET /getAlarme HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        response = ""
        try:
            self.send(request)
            response = self.recive()
            print(response)
        except:
            print(response)
            pass

    def get_fatura(self):
        '''
        Solicita a fatura

        return:

        request - String: Json codificado
        '''
        json_string = {"id":self.cpf}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'GET /getFatura HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request
    
    def cadUser(self,id,name):
        '''
        Cadastra usuário

        Return

        request - String: Json com a requisição
        '''
        json_string = {"id":id,"name":name}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'POST /cadCliente HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request
    
    def cadMedidor(self,id):
        '''
        Cadastrar Medidor

        Arguments:
        id - Int: identificador do medidor

        Retruns - String: Json com a requisição

        '''
        json_string = {"id":id}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'POST /cadMedidor HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request

    
