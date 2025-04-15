import serial #Importa a biblioteca

while True: #Loop para a conexão com o Arduino
    try:  #Tenta se conectar, se conseguir, o loop se encerra
        com = serial.Serial('/dev/ttyUSB0', 115200)
        print('Arduino conectado')
        break
    except:
        pass

while True: #Loop principal
    msg = str(com.readline()) #Lê os dados em formato de string
    msg = msg[2:-5] #Fatia a string
    print(msg) #Imprime a mensagem
    with open('Dados-Teste-Estatico/Calibrar_celula/Dados.txt', 'a') as file:
        file.write(msg + '\n')
    com.flush() #Limpa a comunicação