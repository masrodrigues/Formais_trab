# coding: utf-8
# Artur Bernardo
# Marco Antonio de Souza Rodrigues
# ==========Criação do Grafo=======================
class Grafo:
    def __init__(self):
        self.lista_vizinhos = {}
        self.lista_vertices = {}
    
    def add_vertice(self, vertice):
        self.lista_vertices[vertice] = True
    
    def add_aresta(self, qa, qb, palavra):
        if not qa in self.lista_vizinhos:
            self.lista_vizinhos[qa] = []
        self.lista_vizinhos[qa].append([palavra, qb])
    
    def transicoes(self, qa):
        if qa in self.lista_vizinhos:
            return self.lista_vizinhos[qa]
        else:
            return []
    
    def estados(self):
        return self.lista_vertices.keys()

# ============Leitura do arquivo================
file = open("arquivodeentrada.txt", "r")
words = []
transitions = []
for i in file:
    for word in i.split():
        words.append(word)
file.close()

AFND = words[0]
AFND = AFND.split("{")
estados = AFND[1].split(',')
estados[-1] = estados[-1][:-1]
palavras = AFND[2].split(',')
palavras[-1] = palavras[-1][:-1]
estadoI = AFND[3]
estadoI = estadoI[:-1] 
estadoF = AFND[4].split(',')
estadoF[-1] = estadoF[-1][:-1]

for i in range(2, len(words)):
    transitions.append(words[i])

G = Grafo()
for i in range(0, len(estados)):
    G.add_vertice(estados[i])

for i in range(0, len(transitions)):
    aux = transitions[i].split("=")
    aux[0] = aux[0][1:-1]
    aux[0] = aux[0].split(",")
    G.add_aresta(aux[0][0], aux[1], aux[0][1])

print("AFND: ", AFND)
print("Estados: ", estados)
print("Palavras: ", palavras)
print("Estado inicial: ", estadoI)
print("Estados finais: ", estadoF)
print("Transicoes:", transitions)
print("\n\n")

# ==========Criando AFD============================
afd2 = {}
afd2[estadoI] = True
n = len(afd2.keys())
i = 0

G_AFD = Grafo()
G_AFD.add_vertice(estadoI)
novos_estados_finais = []

while(i < n and n < 70):
    if i >= len(afd2.keys()):
        break
    estadosAFD = list(afd2.keys())
    estadoAux = estadosAFD[i].split(",")
    for j in range(0, len(palavras)):
        new_estado = ""
        for l in range(0, len(estadoAux)):
            transicoes = G.transicoes(estadoAux[l])
            for k in range(0, len(transicoes)):
                if palavras[j] == transicoes[k][0] and transicoes[k][1] not in new_estado:
                    new_estado += transicoes[k][1] + ","
        
        if new_estado != "":
            new_estado = new_estado[:-1]
            afd2[new_estado] = True
            n += 1
            G_AFD.add_vertice(new_estado)
            for e in estadoF:
                aux = new_estado.split(",")
                for m in range(0, len(aux)):
                    if e in aux[m] and new_estado not in novos_estados_finais:
                        novos_estados_finais.append(new_estado)
            G_AFD.add_aresta(estadosAFD[i], new_estado, palavras[j])
    i += 1

print('=======NOVO GRAFO========')
print("Estados finais: ", novos_estados_finais)
print("Transicoes:", transitions)
print("\nEstados:", G_AFD.estados())

# ==========Exibindo o AFD como uma tabela==========
from prettytable import PrettyTable

tabela_transicoes = PrettyTable(['Estado', 'Transições'])
for estado in G_AFD.estados():
    transicoes = ', '.join([f"{tr[0]} -> {tr[1]}" for tr in G_AFD.transicoes(estado)])
    tabela_transicoes.add_row([estado, transicoes])

print("Prog")
print(tabela_transicoes)

# ==========Leitura e teste de sequências do arquivo de teste==========
def ler_sequencias_teste(nome_arquivo):
    try:
        with open(nome_arquivo, "r") as arquivo:
            sequencias = arquivo.readlines()
        return [seq.strip().split(',') for seq in sequencias]
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None

while True:
    nome_arquivo_teste = input("Digite o nome do arquivo de teste: ")
    sequencias_teste = ler_sequencias_teste(nome_arquivo_teste)
    if sequencias_teste is not None:
        break
    else:
        print("Por favor, tente novamente.")

for sequencia in sequencias_teste:
    estadoAtual = estadoI
    resp = True
    invalido = False

    for simbolo in sequencia:
        proximo_estado = False
        for transicao in G_AFD.transicoes(estadoAtual):
            if simbolo == transicao[0]:
                proximo_estado = True
                estadoAtual = transicao[1]
                break
        if not proximo_estado:
            resp = False
            invalido = True
            break

    if estadoAtual in novos_estados_finais and not invalido:
        print(f"\nSequência '{', '.join(sequencia)}': Aceita")
    else:
        print(f"\nSequência '{', '.join(sequencia)}': Rejeita")
    print("\n")
