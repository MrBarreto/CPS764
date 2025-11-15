import requests
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

try:
    response = requests.delete(urlApplication, auth=auth, verify=False)
    response.raise_for_status() 
    print(f"Aplicação desativada\n Codigo: {response.status_code}")
except Exception as e:
    print(f"Erro ao processar a requisição de desligamento: {e}")


topo = CustomTopology()
net = Mininet(topo, controller=None)
net.addController( 'c0', controller=RemoteController, ip='192.168.122.1', port=6653)
net.start()

h1 = net.get('h1')
h2 = net.get('h2')
h4 = net.get('h4')
h7 = net.get('h7')

print("Teste de ping sem intents")

print("\n--- Executando teste de ping (h1 -> h2) ---")
output_t1 = h1.cmd(f'ping -c 3 {h2.IP()}')
print(output_t1)

print("\n--- Executando teste de ping (h4 -> h7) ---")
output_t2 = h4.cmd(f'ping -c 3 {h7.IP()}')
print(output_t2)

intentH1H2 = {
  "type": "HostToHostIntent",
  "appId": "org.onosproject.ovsdb",
  "priority": 55,
  "one": f"{h1.MAC()}/-1",
  "two": f"{h2.MAC()}/-1"
}

intentH4H7 = {
  "type": "HostToHostIntent",
  "appId": "org.onosproject.ovsdb",
  "priority": 55,
  "one": f"{h4.MAC()}/-1",
  "two": f"{h7.MAC()}/-1"
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("Iniciando cricao de intents...")

try:
    response = requests.post(urlIntent, auth=auth, headers=headers, json=intentH1H2 ,verify=False)
    response.raise_for_status() 
    print(f"Intent H1-H2 criado com sucesso\n Codigo: {response.status_code}")
except Exception as e:
    print(f"Erro ao criar intent H1-H2: {e}")

try:
    response = requests.post(urlIntent, auth=auth, headers=headers, json=intentH4H7 ,verify=False)
    response.raise_for_status() 
    print(f"Intent H4-H7 criado com sucesso\n Codigo: {response.status_code}")
except Exception as e:
    print(f"Erro ao criar intent H4-H7: {e}")

time.sleep(5)
print("Realizando testes com intents criados...")

print("\n--- Executando teste de ping (h1 -> h2) ---")
output_t1 = h1.cmd(f'ping -c 3 {h2.IP()}')
print(output_t1)

print("\n--- Executando teste de ping (h4 -> h7) ---")
output_t2 = h4.cmd(f'ping -c 3 {h7.IP()}')
print(output_t2)

net.stop()