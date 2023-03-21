import datetime

class Cliente:
    clientes_id = []

    def __init__(self,id,name):
        self.id = 0
        self.name = name
        self.medidores = {}
        self.last_fatura = 0
        self.last_consumo = 0

        if id not in self.clientes_id:
            self.id = id
            self.clientes_id.append(id)

    class __Medidor:
        def __init__(self,id):
            self.id = id
            self.medicoes = []
          #  self.medicoes.append(('timestamp','Value'))
        
    
    @classmethod
    def add_Clientes_by_file(cls,url):
        with open(url,'r') as ark:
            pass
    @classmethod
    def add_Clientes(cls,id,name):
        pass


    def add_new_medidor(self):
        id = str(len(self.medidores) + 1)
        self.medidores[id] = self.__Medidor(id)
    
    def update_value(self,id,value,timestamp):
        print(self.medidores)
        self.medidores[id].medicoes.append((timestamp,value))


    def get_fatura(self):
        #Valor utilizado foi de 1,07 reais, no qual compoe a media nacional
        #consumo = []
        soma = 0
        data_atual = datetime.datetime.now()

        
        for id,medidor in self.medidores.items():
            print(medidor.medicoes)
            for timestamp,value in medidor.medicoes:
                print(f'{id},{timestamp},{type(timestamp)},{repr(timestamp)}')
                data_timestamp = datetime.datetime.fromtimestamp(float(timestamp))
                if  data_timestamp.month == data_atual.month and data_timestamp.year == data_atual.year:
                    #consumo.append(timestamp,value)
                    soma+= float(value)

        return (soma*1.07,soma)
        
    def get_consumo(self,kind,periodo):
        consumo = []
        soma = 0
        consumo.append(('timestamp','value'))
        for id,medidor in self.medidores.items():
            for timestamp,value in medidor.medicoes:
                #print(f"Erros : {timestamp}")
                data_timestamp = datetime.datetime.fromtimestamp(float(timestamp))
                if kind=='D':
                    if datetime.datetime.now().day - data_timestamp.day == periodo:
                        timestamp_convertido = datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M")
                        consumo.append((timestamp_convertido,value))
                        soma += float(value)
                elif kind == 'M':
                    print("entrei aqui")
                    if datetime.datetime.now().month - data_timestamp.month == periodo:
                        timestamp_convertido = datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M")
                        consumo.append((timestamp_convertido,value))
                        soma+=float(value)
                elif kind == 'Y':
                    if datetime.datetime.now().year - data_timestamp.year == periodo:
                        timestamp_convertido = datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M")
                        consumo.append((timestamp_convertido,value))
                        soma+=float(value)
                else:
                    return consumo
        print("Consumo solicitado:\n")
        print(consumo)
        return (soma,consumo)
    
    def get_alarme(self):
        valor_acumulado,consumo_acumulado = self.get_consumo('M',0)
        if valor_acumulado > 1000:
            return {'alarme':'Excesso!'}
        for timestamp,consumo in consumo_acumulado[1:]:
            if consumo > 1000:
                return {'alarme':'Excesso!'}
        return {'alarme':'Ok!'}




    



    
    