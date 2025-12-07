#!/bin/bash

echo "[INFO] Iniciando configuracao de rede..."

# ------------------------------------------------------------
# 1. Definindo Funcoes (Linux e OVS)
# ------------------------------------------------------------

clean_veth() {
    ip link show $1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[CLEAN] Removendo interface antiga: $1"
        ip link delete $1
    fi
}

create_linux_bridge() {
    brctl show | grep -q "^$1"
    if [ $? -ne 0 ]; then
        echo "[SETUP] Criando Linux Bridge: $1"
        brctl addbr $1
        ip link set $1 up
    else
        echo "[INFO] Linux Bridge $1 ja existe."
        ip link set $1 up
    fi
}

create_ovs_bridge() {
    ovs-vsctl show | grep -q "$1"
    if [ $? -ne 0 ]; then
        ovs-vsctl add-br $1
        ovs-vsctl set-fail-mode $1 secure
        ovs-vsctl set-controller $1 tcp:192.168.122.1:6653
        ovs-vsctl set bridge $1 protocols=OpenFlow13
        ip link set $1 up
    else
        echo "[INFO] OVS Bridge $1 ja existe. Pulando configuracao."
    fi
}

# ------------------------------------------------------------
# 1. Preparação das Bridges (Linux e OVS)
# ------------------------------------------------------------
create_linux_bridge "br-lxc-server"

create_ovs_bridge "ovs-dr"


# ------------------------------------------------------------
# 2. Conexão: Servidor (LXC) <-> OVS Server
# ------------------------------------------------------------
echo "[SETUP] Configurando conexao do Lado Servidor..."

clean_veth "veth-br-server"
clean_veth "veth-ovs-dr"

ip link add veth-br-server type veth peer name veth-ovs-dr

brctl addif br-lxc-server veth-br-server
ip link set veth-br-server up

ovs-vsctl --may-exist add-port ovs-dr veth-ovs-dr
ip link set veth-br-server up

echo "[SUCCESS] Configuração concluída com sucesso!"
