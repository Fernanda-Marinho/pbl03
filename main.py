import sys 
import os
import pickle
from funcoes import *

"""Autor: Fernanda Marinho Silva
Componente Curricular: MI - Algoritmos I
Concluido em: 01/07/2022
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação."""


localMain = os.getcwd() #O arquivo binário do indice invertido será salvo nesse local

"""Iniciação do dicionario de indice invertido
podendo ser vazio ou não."""
conteudoDoIndice = indiceConteudo() 
if conteudoDoIndice == True:
    indiceI = open("IndiceInvertido.pkl",'rb')
    dicIndiceInvertido = pickle.load(indiceI) 
else: 
    indiceI = open("IndiceInvertido.pkl",'ab')
    dicIndiceInvertido = {}

validArgumentos = verificaArgumentos(1)
if validArgumentos != False:
    arg = sys.argv[1].lower()
    if arg == "add":

        """Uma nova verificação é feita, pois o usuário pode digitar apenas
        o add, sem informar o diretório"""
        validArgumentos = verificaArgumentos(2) 

        if validArgumentos != False:
            dirExiste = existe(sys.argv[2])
            if dirExiste:
                dirIndexado, dirArquivo = jaIndexado(sys.argv[2],dicIndiceInvertido)

                """Caso o diretório seja novo, será indexado ao indice
                e caso contrário, ocorre a atualização dele."""
                if dirIndexado:
                    print("Humm... Este diretório já foi indexado :( Mas não se preocupe, iremos atualizar ele! :)")
                    dicIndiceInvertido = remove(arg,sys.argv[2],dicIndiceInvertido)
                    os.chdir(sys.argv[2])  
                    l = arquivosNoDiretorio(sys.argv[2])
                    for i in l:
                        dicIndiceInvertido = indiceInvertido(dicIndiceInvertido,i,sys.argv[2],localMain)
                else:
                    print("Opaaa! Diretório novo :)")
                    os.chdir(sys.argv[2])  
                    l = arquivosNoDiretorio(sys.argv[2])
                    for i in l:
                        dicIndiceInvertido = indiceInvertido(dicIndiceInvertido,i,sys.argv[2],localMain)
                                
            else: #Diretório não existe 
                print("O diretório inserido não existe no seu computador :(")
                print("Iremos mostrar ajuda:\n")
                mostraAjuda()
        
    elif arg == "remove":

        """Uma nova verificação é feita, pois o usuário pode digitar apenas
        o remove, sem informar o diretório ou arquivo para remover"""
        validArgumentos = verificaArgumentos(2)

        if validArgumentos != False:
            dicIndiceInvertido = remove(arg,sys.argv[2],dicIndiceInvertido)
    
    elif arg == "update":

        """Uma nova verificação é feita, pois o usuário pode digitar apenas
        o update, sem informar o diretório ou arquivo para atualizar"""
        validArgumentos = verificaArgumentos(2)

        if validArgumentos != False:
            indexado, dirArquivo = jaIndexado(sys.argv[2],dicIndiceInvertido)
            if indexado:
                dicIndiceInvertido = remove(arg,sys.argv[2],dicIndiceInvertido)
                os.chdir(dirArquivo) 
                l = arquivosNoDiretorio(dirArquivo)
                for i in l:
                    dicIndiceInvertido = indiceInvertido(dicIndiceInvertido,i,dirArquivo,localMain)
                print("Prontinho! Informações atualizadas :)")
            else:
                print("Vishh... Esse arquivo/diretório não foi encontrado! Sinto muito.")
                print("Aqui vai uma ajuda:\n")
                mostraAjuda()

    elif arg == "search":

        """Uma nova verificação é feita, pois o usuário pode digitar apenas
        o search, sem informar a palavra-chave a ser buscada"""
        validArgumentos = verificaArgumentos(2)

        if validArgumentos != False:
            palavraChave = sys.argv[2].lower() 
            a = busca(palavraChave,dicIndiceInvertido)
            resultadoBusca(a,palavraChave)
    
    elif arg == "view": #Visualização do indice invertido 
        mostraIndice(dicIndiceInvertido)
    
    else: #Provavel erro no usuário 
        print("Hummm... Parece que você digitou alguma coisa errada. Aqui vai uma ajuda:\n")
        mostraAjuda()
    
    """Após feitas as operações do usuário, o programa salva 
    possíveis alterações no arquivo binário e fecha o mesmo."""
    indiceI = open("IndiceInvertido.pkl",'wb')
    pickle.dump(dicIndiceInvertido,indiceI)
    indiceI.close()