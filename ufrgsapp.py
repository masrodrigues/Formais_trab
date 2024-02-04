# coding: utf-8
#Artur Bernardo
#Marco Antonio de Souza Rodrigues
#==========Criação do Grafo=======================
class Grafo:
    def __init__(self):
        self.lista_vizinhos = {}
        self.lista_vertices = {}
    
    def add_vertice(self, vertice):
        self.lista_vertices[vertice] = True
    
    def add_aresta(self, qa, qb, palavra):
    	#se nao existe estado qa nao add
        if not qa in self.lista_vizinhos:
            self.lista_vizinhos[qa] = []
        #add qb e w como uma transicao de qa
        self.lista_vizinhos[qa].append([palavra,qb])
    
    def transicoes(self, qa):
        if qa in self.lista_vizinhos:
        	#retorna as transicoes de um estado qa
            return self.lista_vizinhos[qa]
        else:
            return []
    
    def estados(self):
        return self.lista_vertices.keys()

    def deleta_aresta(self, vertice, outro_vertice):
        self.vizinhos(vertice).remove(outro_vertice)
    
    def deleta_vertice(self, vertice):
        for outro_vertice in self.lista_vizinhos[vertice]:
            self.deleta_aresta(vertice, outro_vertice)
        del self.lista_vizinhos[vertice]
        del self.lista_vertices[vertice]
        
# ============Leitura do arquivo================
file = open("arquivodeentrada.txt", "r")
words = []
transitions = []
#Leitura do arquivo
for i in file:
    for word in i.split():
        words.append(word)

#Organização do arquivo
AFND = words[0]

AFND = AFND.split("{")
estados = AFND[1].split(',')
estados[-1] = estados[-1][:-1]#le os estados corretamente
palavras = AFND[2].split(',')
palavras[-1] = palavras[-1][:-1]#le as palavras corretamente
estadoI = AFND[3]
estadoI = estadoI[:-1] 
estadoF = AFND[4].split(',')
estadoF[-1] = estadoF[-1][:-1]#le os estados finais corretamente

for i in range (2, len(words)):
    transitions.append(words [i])

G = Grafo()
#============Criando AFND=======================

#adiciona os estados no grafo
for i in range (0, len(estados)):
	G.add_vertice(estados[i])

#add transicoes no grafo (qa -> qb)
for i in range (0, len(transitions)):
	#quebra a string -> aux[0] = (qa,w) e aux[1] = qb
	aux = transitions[i].split("=")
	#retira parenteses
	aux[0] = aux[0][1:]
	aux[0] = aux[0][:-1]
	#quebra a string em qa e w
	aux[0] = aux[0].split(",")
	#add transicao
	G.add_aresta(aux[0][0],aux[1],aux[0][1])
	
#AFND
print ("AFND: ",AFND)
print ("Estados: ",estados)
print ("Palvras: ",palavras)
print ("Estado inicial: ",estadoI)
print ("Estados finais: ",estadoF)
print ("Transicoes:",transitions)
print ("")
print ("")


# ==========Criando AFD============================
print()
print()

afd2 = {}
afd2[estadoI] = True
n = len(afd2.keys())
i = 0

G_AFD = Grafo()             #instancia um novo grafo AFD 
G_AFD.add_vertice(estadoI)  #add o estado inicial no novo grafo AFD
novos_estados_finais = []   #lista de estados finais do AFD


while(i < n and n < 70):# Converte AFND para AFD enquanto já cria o novo grafo AFD
    if (i >= len(afd2.keys())): break;
    estadosAFD = list(afd2.keys())
    estadoAux = estadosAFD[i].split(",") #quebra o estado em virgulas
    for j in range(0, len(palavras)):
        new_estado = ""
        for l in range(0, len(estadoAux)):
            transicoes = G.transicoes(estadoAux[l])
            for k in range(0, len(transicoes)):
                if (palavras[j] == transicoes[k][0]) and (transicoes[k][1] not in new_estado):
                    new_estado += transicoes[k][1] + ","
        
        if (new_estado != ""):
            new_estado = new_estado[:-1] #retira a ultima virgula
            afd2[new_estado] = True #adiciona o novo estado no afd2
            n += 1
            #add no grafo (new_estado)
            G_AFD.add_vertice(new_estado)


            #Estados finais  
            for e in estadoF:
                aux = new_estado.split(",")
                for m in range(0, len(aux)):
                    if (e in aux[m]) and (new_estado not in novos_estados_finais):
                        novos_estados_finais.append(new_estado)

            #add aresta (estadosAFD[i]  ==palavras[j]==>  new_estado)
            G_AFD.add_aresta(estadosAFD[i], new_estado, palavras[j])
            
    i += 1
               
print('=======NOVO GRAFO========')

print ("Estados finais: ",novos_estados_finais)
print ("Transicoes:",transitions)
print ("")
print("Estados:",G_AFD.estados())
print("Prog")
#Novas transiçoes
for m in G_AFD.estados():
    print (m, ": ", G_AFD.transicoes(m))
    

## Função para ler as sequências de símbolos do arquivo de teste
def ler_sequencias_teste(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        sequencias = arquivo.readlines()
    return [seq.strip().split(',') for seq in sequencias]
print ('\n')
cont = 's'
while(cont == 's' or cont == 'S'):
    # Função para ler as palavras do arquivo de teste


# Solicitar ao usuário para digitar o nome do arquivo de teste
    nome_arquivo_teste = input("Digite o nome do arquivo de teste: ")
    sequencias_teste = ler_sequencias_teste(nome_arquivo_teste)

# Testar cada sequência de símbolos do arquivo de teste
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
            print(f"Sequência '{', '.join(sequencia)}': Aceita")
        else:
            print(f"Sequência '{', '.join(sequencia)}': Rejeita")
        print("\n")


    cont = input("\nDeseja inserir uma nova palavra(S/N): ")
    print("\n")
