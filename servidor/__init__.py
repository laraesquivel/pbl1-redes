#Pertencente a Lara Esquivel de Brito Santos
#from dotenv import load_dotenv
import socket, threading
import os,sys, signal
from server import Server


def handler():
    sys.exit(0)


#load_dotenv()
#print(os.environ['PORT'])
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tipo de endereco / tipo de soquete
#org = ((os.environ['HOST']), (os.environ['PORT']))

servidor = Server(host=socket.gethostbyname(socket.gethostname()))
servidor.start()
signal.signal(signal.SIGINT,handler)



