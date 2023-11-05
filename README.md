# Proxy

Proxy para intermediar a comunicação entre aplicações e dispositivos IoT

## Requisitos

* Instalar Python3.10 ou superior ([tutorial](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/))
```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

## Para executar o Proxy, informe o IP e a Porta do servidor (ex: 127.0.0.1 se for executar em localhost)
```
python3 src/main.py -a <IP_ADDRESS_OR_URL> -p <PORT>
```


