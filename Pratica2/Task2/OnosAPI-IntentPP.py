import requests
import time
from mininet.net import Mininet
from mininet.node import RemoteController
from CustomTopology import CustomTopology

def getHostInformation(MAC, auth):
    MAC.replace(':', '%')
    urlHosts = f"http://192.168.122.1:8181/onos/v1/hosts/{MAC}/-1"
    header = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(urlHosts, auth=auth, headers=header, verify=False)
        response.raise_for_status() 
        print(f"Detalhes do Host obtidos com sucesso\n Codigo: {response.status_code}")
    except Exception as e:
        print(f"Falha ao consultar detalhes do host: {e}")
    data = response.json()
    return data["locations"][0]["elementId"], data["locations"][0]["port"]

def createPointtoPointIntent(h1_info, h2_info, auth):
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }   
    
    body = {
        "type": "PointToPointIntent",
        "appId": "org.onosproject.ovsdb",
        "priority": 55,
        "ingressPoint": {
            "device": h1_info[0],
            "port": h1_info[1]
        },
        "egressPoint": {
            "device": h2_info[0],
            "port": h2_info[1]
        }
    }
    
    urlIntent = f"http://192.168.122.1:8181/onos/v1/intents"

    try:
        response = requests.post(urlIntent, auth=auth, headers=headers, json=body ,verify=False)
        response.raise_for_status() 
        print(f"Intent criado com sucesso\n Codigo: {response.status_code}")
    except Exception as e:
        print(f"Erro ao criar intent: {e}")

ONOS_IP = "192.168.122.1"
ONOS_USER = "onos"
ONOS_PASS = "rocks"

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

h1_info = getHostInformation(h1.MAC(), auth)
h2_info = getHostInformation(h2.MAC(), auth)
h4_info = getHostInformation(h4.MAC(), auth)
h7_info = getHostInformation(h7.MAC(), auth)

print("Iniciando criacao de intents...")

createPointtoPointIntent(h1_info, h2_info, auth)
createPointtoPointIntent(h2_info, h1_info, auth)
createPointtoPointIntent(h4_info, h7_info, auth)
createPointtoPointIntent(h7_info, h4_info, auth)

time.sleep(5)
print("Realizando testes com intents criados...")

print("\n--- Executando teste de ping (h1 -> h2) ---")
output_t1 = h1.cmd(f'ping -c 3 {h2.IP()}')
print(output_t1)

print("\n--- Executando teste de ping (h4 -> h7) ---")
output_t2 = h4.cmd(f'ping -c 3 {h7.IP()}')
print(output_t2)

net.stop()