import sys 
import os
import pickle



"""Não recebe parâmetro e retorna um valor booleano
Ela tenta carregar os dados de um arquivo binário 
Caso consiga (True) -> arquivo binário tem coisa 
Caso não consiga (False) -> arquivo binário vazio
"""
def indiceConteudo():
    try:
        indiceI = open("IndiceInvertido.pkl",'rb')
        pickle.load(indiceI)
        return True
    except:
        return False 


"""Recebe um inteiro e retorna um booleano ou None.
Verifica se o usuário digitou a quantidade de
argumentos por linha de comando corretamente."""
def verificaArgumentos(n):
    if len(sys.argv) == n:
        print("Hummm... Parece que você digitou alguma coisa errada. Aqui vai uma ajuda:\n")
        mostraAjuda()
        return False 


"""Recebe um diretório e retorna um valor booleano
Verifica se determinado diretório existe no computador
Se existir, v recebe True. Se não, False."""
def existe(doc):
    v = os.path.exists(doc)
    return v


"""Recebe um arquivo ou diretório podendo retornar dois booleanos
ou um booleano e uma posição.
A função verifica se o arquivo/diretório está no dicionário do indice invertido.
Caso esteja, retorna True e a posição que contém o diretório (essa posição será
importante em determinados casos). Caso não esteja, retorna False e False"""
def jaIndexado(info,dic):
    booleano = False 
    posicao = False 
    for i in dic:
        for j in dic[i]:
            if info in j: 
                booleano = True 
                posicao = j[1]
    return booleano, posicao 


"""Recebe o argumento do usuário (remove, update, etc...), o arquivo
ou diretório que deseja remover e o dicionário do indice invertido.
Percorre todo o indice e remove tudo que tem o diretório ou arquivo 
desejado. 
Retorna o dicionário do indice invertido com as remoções atualizadas."""
def remove(argumento,info,dic):
    cont = 0
    for i in dic.copy():
        for j in dic[i].copy():
            if info in j: #Se sim, há remoção pra fazer 
                cont += 1 
                if len(dic[i]) == 1: #Chave presente APENAS no diretório/arquivo a ser removido 
                    del dic[i] 
                else: #Há outras ocorrências em outros arquivos/diretórios
                    local = dic[i].index(j) 
                    dic[i].pop(local) #Remove a posição que contém apenas diretório/arquivo a ser removido  
    if argumento == "remove":
        if cont == 0: #Não houve nenhuma remoção 
            print("Vishh... Esse arquivo/diretório não foi encontrado! Sinto muito.")
            print("Aqui vai uma ajuda:\n")
            mostraAjuda()
        else:
            print("Removido!")
    return dic


"""Recebe um diretório e retorna uma lista com todos os arquivos
formato (.txt) presentes no mesmo."""
def arquivosNoDiretorio(d):
    lista = []
    for arquivo in os.listdir(d):
        if arquivo.endswith(".txt"):
            lista.append(arquivo)
    return lista


"""Recebe o dicionário de indice invertido, o caminho do arquivo (.txt), o diretório 
onde ta aquele arquivo e o diretório deste código.
A função faz um indice invertido e retorna o dicionário desse indice (que pode estar
vazio ou conter elementos dentro dele)"""
def indiceInvertido(dic,arq,dir,loc):  
    documento = str(dir)+'\\'+str(arq)
    caminArq = f"{dir}\{arq}"
    try: 
        with open(documento, 'r') as f:  
            for linha in f: 
                for palavra in linha.split():  
                    if palavra.isalpha() == False: #Tem caractere especial no meio da palavra
                        palavra = pontuacao(palavra) #Tira o caractere especial
                    if palavra != "": 
                        os.chdir(loc) #Indice ficará salvo na mesma pasta deste código 
                        lista = []
                        if palavra.lower() not in dic: #Significa que a palavra é nova no índice  
                            dic[palavra.lower()] = [[caminArq,dir, 1]] #Apenas cria uma chave nova
                        else: #Palavra já existe no índice  
                            for i in dic[palavra.lower()]: 
                                lista.append(i[0]) #Lista com todos os arquivos(.txt) que essa palavra tem 
                            if caminArq not in lista: #A palavra aparece no arquivo(.txt) pela primeira vez
                                dic[palavra.lower()].append([caminArq,dir, 1]) 
                            else: #A palavra repete no arquivo(.txt) 
                                localizacao = lista.index(caminArq)
                                dic[palavra.lower()][localizacao][2] += 1
    except: 
        #Se tiver algum arquivo corrompido, irá ignorar 
        pass 
    return dic


#Recebe uma palavra com um caractere especial e retorna ela sem
def pontuacao(p): #p = palavra 
    caracteres = '''!()-[]{};:¨'"\, <>./?@#$%^&*_'''
    for i in p:
        if i in caracteres:
            p = p.replace(i,"")
            p = p.lower().strip()
    return p


"""Recebe uma palavra e o dicionário do indice invertido
Tenta retornar o valor da chave correspondente a essa palavra
Caso não consiga, retorna False"""
def busca(termo,dic):
    try:
        return dic[termo]
    except KeyError:
        return False


"""Recebe o resultado se a busca existe ou não e a palavra que foi buscada
Caso a palavra buscada exista no indice, printa as ocorrências da palavra,
caso contrário, é avisado que a palavra não foi encontrada. Não retorna nada."""
def resultadoBusca(resultado,palavra):
    if resultado != False:
        cont = 0 
        ord = sorted(resultado, key=lambda x:x[2],reverse=True) #Ordena decrescente com base no número de ocorrências por arquivo 
        print(f"A palavra [ {palavra} ] aparece nos seguintes documentos:")
        for i in ord:
            print(f"Documento -> {i[0]} | Quantidades de vezes -> {i[2]}")
            cont += 1
        print(f"Ao todo, a palavra foi encontrada em {cont} documentos!")
        
    else:
        print(f"Sinto muito, a palavra [ {palavra} ] não foi encontrada!")


"""Não recebe nenhum parâmetro e exibe ajuda ao usuário
caso ele digite algo errado. Não retorna nada."""
def mostraAjuda():
    print("\t= = = A J U D A = = =")
    print("-"*60)
    print("PARA ADICIONAR UM DIRETÓRIO:")
    print("_"*60)
    print(">>> python main.py add (*diretório desejado*)")
    print("_"*60)
    print("\nOBS:Caso o diretório já tenha sido adicionado, iremos")
    print("atualizar as informações de TODOS OS ARQUIVOS (formato* txt)") 
    print("presentes no diretório!")
    print("Porém você atualizar seus dados de forma específica,") 
    print("seguindo a dica abaixo:")
    print("-"*60)
    print("PARA ATUALIZAR UM DIRETÓRIO OU ARQUIVO:")
    print("_"*60)
    print(">>> python main.py update (*diretório ou arquivo desejado*)")
    print("_"*60)
    print("\nOBS:Caso escolha atualizar somente um arquivo, deverá digitar")
    print("o caminho completo! Exemplo:\nC:\\Users\\diretorio\\laudos.txt")
    print("-"*60)
    print("PARA REMOVER UM DIRETÓRIO OU ARQUIVO:")
    print("_"*60)
    print(">>> python main.py remove (*diretório ou arquivo desejado*)")
    print("_"*60)
    print("\nOBS:As mesmas observações da dica anterior se aplicam à esta!")
    print("-"*60)
    print("PARA REALIZAR A BUSCA DE UMA PALAVRA-CHAVE:")
    print("_"*60)
    print(">>> python main.py search (*palavra desejada*)")
    print("_"*60)
    print("-"*60)
    print("PARA VISUALIZAR O ÍNDICE INVERTIDO:")
    print("_"*60)
    print(">>> python main.py view")
    print("_"*60)


"""Recebe o dicionario do indice invertido como parâmetro
apenas printa o indice invertido. Não retorna nada"""
def mostraIndice(dic):
    print("\t = = = ÍNDICE INVERTIDO = = = \n")
    print(dic)
    print("\n\t = = = FIM DO ÍNDICE INVERTIDO = = = ")