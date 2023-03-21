import socket,threading
import json
import schedule,time

class Cliente:
    def __init__(self,cpf,medidores,minutes=3,host="localhost",port=8888):
        self.cpf = cpf
        self.medidores = medidores 
        self.host = host
        self.port = port
        self.cliente = None
        self.minutes = minutes
    
    def start(self):
        schedule.every(self.minutes).minutes.do(self.get_alarm)
        t = threading.Thread(target=self.run_schedule)
        t.start()

    def run_schedule(self):
        schedule.run_pending()
        time.sleep(1)
    
    def connect(self):
        self.cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cliente.connect((self.host,self.port))

    def send(self,request):
        self.cliente.sendall(request.encode())
    
    def recive(self):
        response = self.cliente.recv(1024)
        response = response.decode()
        return response

    def get_historico(self,medidor_id,kind,periodo):
        m = self.medidores[medidor_id-1]
        json_string = {"id":self.cpf,"id_medidor":m,"kind":kind,"periodo":periodo}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'GET /getConsumoHist HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request
    
    def get_alarm(self):
        json_string = {"id":self.cpf}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        print("Estou solicitando alarme...")
        request = f'GET /getAlarme HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        try:
        
            self.send(request)
            response = self.recive()
            print(response)
        except:
            pass

    def get_fatura(self):
        json_string = {"id":self.cpf}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'GET /getFatura HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request
    
    def cadUser(self,id,name):
        json_string = {"id":id,"name":name}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'POST /cadCliente HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request
    
    def cadMedidor(self,id):
        json_string = {"id":id}
        json_string = json.dumps(json_string,separators=(',',':'),indent='\t')
        size = len(json_string)
        request = f'POST /cadMedidor HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nUser-Agent: EsquivelWindows10NT/2022.7.5\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: {size}\r\n\r\n{json_string}'
        return request

    
