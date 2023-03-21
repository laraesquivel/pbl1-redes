
import threading, socket
import view, json
import asyncio

class Server:
    def __init__(self,host='localhost',port= 8888, udp_port = 8080):
        self.__host = host
        self.__port = port
        self.__udp_port = udp_port
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        self.__run_server = True

        self.server_socket.bind((host,port))
        self.server_udp.bind((host,udp_port))
        
        self.server_socket.listen()
    
    def start(self):
        while True:
            thread_tcp = threading.Thread(target=self.start_tcp)
            thread_tcp.start()

            msg, addr = self.server_udp.recvfrom(1024)
            thread_udp = threading.Thread(target=self.handle_connnection_udp,args=(msg,addr))
            thread_udp.start()

    def start_tcp(self):
         while self.__run_server:
            conex, addr = self.server_socket.accept()
            print(f'Conectado de {addr}')
            thread = threading.Thread(target= self.handle_connection, args=(conex, addr))
            thread.start()

    def handle_connnection_udp(self,msg,addr):
        print(f'Mensagem de {addr} Recebida {repr(msg.decode())}')
        valor = (msg.decode()).split(',')
        print(valor)
        view.post_consumo(valor[0],valor[1],valor[2],valor[3])
        response = "200"
        self.server_udp.sendto(response.encode(),addr)

    def handle_connection(self,conex,addr):
        with conex:
            print(conex)
            request = conex.recv(1024).decode()
            print(repr(request))
            response = 'HTTP/1.1 404 Not Found\r\nContent-Length: 9\r\n\r\nNot found'
            if request:
                method, path, *restante = request.split(' ')
                if path != '/':
                    print(f'Esse é o resto : {restante}')
                    x = json.loads((((restante[5]).split("\r\n\r\n"))[1]).strip('\n').strip('\t'))
                    print(f'Json: {x}')
                if path == '/' and method=='GET':
                    body = json.dumps(view.get_home())
                    length = len(body)
                    response = f'HTTP/1.1 200 OK\r\nContent-Length: {length}\r\n\r\n'+body

                elif method== 'GET' and path == '/about':
                    response = view.get_clientes()
                    conex.sendall(response.encode())

                elif path == '/cadCliente' and method == 'POST': 
                    x = dict(x)
                    print(x['id'],x['name'])
                    response = view.cad_cliente(x['id'],x['name'])
                    conex.sendall(response.encode())
                
                elif path == '/cadMedidor' and method == 'POST':
                    x = dict(x)
                    response = view.cad_medidor(x['id'])
                    conex.sendall(response.encode())
                
                elif path == '/postConsumo' and method == 'POST':
                    x = dict(x)
                    response = view.post_consumo(x['id'],x['id_medidor'],x['valor'],x['timestamp'])
                    conex.sendall(response.encode())
                
                elif path == '/getAlarme' and method == 'GET':
                    x = dict(x)
                    response = view.get_excesso(x['id'])
                    conex.sendall(response.encode())

                elif path == '/getConsumoHist' and method == 'GET':
                    x = dict(x)
                    response = view.get_consumo_geral(x['id'],x['periodo'],x['kind'])
                    conex.sendall(response.encode())
                elif path =='/getFatura' and method == 'GET':
                    x= dict(x)
                    response = view.get_fatura(x['id'])
                    conex.sendall(response.encode())
                else:
                    response = 'HTTP/1.1 404 Not Found\r\nContent-Length: 9\r\n\r\nNot found'
            conex.sendall(response.encode())
        print(f"Fim na conexão {addr}!")

    def server_forever(self):
        pass
    
    def stop(self,signum,frame):
        self.server_socket.close()
        print('Serivdor Encerrado')
