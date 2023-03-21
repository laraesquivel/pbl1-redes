from cliente import Cliente
import view

lara = Cliente(86453121581,'Lara')
assert lara.id == 86453121581

print(view.cad_cliente(234,'Antonie'))
assert len(view.clientes) > 0

lara.add_new_medidor()

lara.update_value(1,2.3,"1677783600")

print(lara.medidores.get(1).medicoes)

lara.get_alarme()
lara.get_consumo('D',167783600)

lara.update_value(1,2.3,"1677783600")
lara.update_value(1,2245.3,"1677783600")
lara.get_alarme()
