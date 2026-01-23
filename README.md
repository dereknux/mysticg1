# Water Cooler Mystic G1 — 'LCD' Controller for Linux

Driver open-source em Python para exibir a temperatura da CPU no display 'LCD' do
watercooler **Mancer Mystic G1**, utilizando USB HID.

Não requer drivers proprietários nem software Windows.

---

## Features

- Exibe temperatura da CPU em tempo real no 'LCD'
- Comunicação direta via USB HID
- Pode rodar como serviço `systemd` (opcional)
- Baixíssimo uso de recursos
- Funciona inteiramente em user-space

---

## Requirements

- Linux com `systemd`
- `python3`
- Mystic G1 conectado via USB interno

---

## Python dependency

Tente primeiro o pacote da distro:

    sudo apt install python3-hid

Se não existir:

    sudo pip3 install hidapi

---

## Installation

### 1. Clone o repositório

    git clone https://github.com/dereknux/mysticg1.git
    cd mysticg1

---

### 2. Permissões USB (udev)

    sudo cp 9-mysticg1.rules /etc/udev/rules.d/
    sudo udevadm control --reload
    sudo udevadm trigger

Desconecte e reconecte o cabo USB do cooler.

---

### 3. Teste manual

    python3 mysticg1.py

Se o LCD acender e mostrar a temperatura, está funcionando.

---

## systemd (opcional)

Instalação como serviço:

    sudo mkdir -p /opt/mysticg1
    sudo cp mysticg1.py /opt/mysticg1/
    sudo cp mysticg1.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now mysticg1.service

Verificar status:

    systemctl status mysticg1.service

---

## Troubleshooting

### ModuleNotFoundError: No module named 'hid'

A dependência HID não está instalada.  
Instale `python3-hid` ou `hidapi` via pip.

---

### OSError: open failed

Erro de permissão USB.  
Verifique se a regra udev foi copiada corretamente e se o dispositivo foi
reconectado.

---

## Technical details

USB Vendor ID:  
    0xaa88

USB Product ID:  
    0x8666

Protocolo: relatório HID de 6 bytes

    [0x00, temperature, 0x00, 0x00, 0x00, checksum]
    checksum = sum(first_5_bytes) & 0xFF

Fonte da temperatura:

    /sys/class/thermal/thermal_zone0/temp

Intervalo de atualização:  
    500 ms (necessário para keep-alive do display)

---

## License

GNU GPLv3
