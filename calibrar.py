data = []
arq = open('Analise de dados/Dados.txt', 'r').read()
lines = arq.split('\n')
for line in lines:
    data.append(line)

soma = 0
for i in range(len(data)):
    soma+=float(data[i])

media = soma/len(data)

peso = int(input('Digite o peso real do objeto: '))

calibracao = media/peso

print('O fator de calibração é: ', calibracao)
arq.close()
