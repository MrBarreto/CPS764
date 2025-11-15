import requests
import json
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from CustomTopology import CustomTopology

ONOS_IP = "192.168.122.1"
ONOS_USER = "onos"
ONOS_PASS = "rocks"

urlIntent = f"http://192.168.122.1:8181/onos/v1/intents"
urlApplication = f"http://192.168.122.1:8181/onos/v1/applications/org.onosproject.fwd/active"

auth = (ONOS_USER, ONOS_PASS)

print(f"Desabilitando Reactive Forwarding...")

try:
    response = requests.delete(urlApplication, auth=auth, verify=False)
    response.raise_for_status() 
    print(f"Aplicação desativada\n Codigo: {response.status_code}")
except Exception as e:
    print(f"Erro ao processar a requisição de desligamento: {e}")


topo = CustomTopology()
net = Mininet(topo, controller=None)
net.addController( 'c0', controller=RemoteController, ip='192.168.122.1', port=6653)

print("Iniciando a topologia")
net.start()
time.sleep(5)

h1 = net.get('h1')
h2 = net.get('h2')
h4 = net.get('h4')
h7 = net.get('h7')

print("Iniciando teste com Reactive Forwarding desligado")
print("\n--- Executando teste de ping (h1 -> h2) ---")

output_t1 = h1.cmd(f'ping -c 3 {h2.IP()}')
print(output_t1)

print("\n--- Executando teste de ping (h4 -> h7) ---")
output_t2 = h4.cmd(f'ping -c 3 {h7.IP()}')
print(output_t2)

print("Ativando reactive Forwarding...")

headers = {
    'Accept': 'application/json'
}

try:
    response = requests.post(urlApplication, auth=auth, headers=headers, verify=False)
    response.raise_for_status() 
    print(f"Aplicação Ativada\n Codigo: {response.status_code}")
except Exception as e:
    print(f"Erro ao processar a requisição de ligação: {e}")

print("Iniciando teste com Reactive Forwarding ligado")

print("\n--- Executando teste de ping (h1 -> h2) ---")
output_t1 = h1.cmd(f'ping -c 3 {h2.IP()}')
print(output_t1)

print("\n--- Executando teste de ping (h4 -> h7) ---")
output_t2 = h4.cmd(f'ping -c 3 {h7.IP()}')
print(output_t2)

net.stop()