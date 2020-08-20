# To do
# - Translate everything
# - Comment
# - Beatiful GUI

from random import uniform as random
import os
import time
import textwrap
import math
from operator import itemgetter
from numpy import log as ln
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import re

def file_creator (data):
    [contador, area, mac, b, chord_1, offset_1, env_1, chord_2, offset_2, env_2, chord_3, offset_3, env_3, chord_4] = data
    o  = open("asa%d.avl" %contador, "w")
    o.write(" Urutau 2019 (2)\n" +
    "0.0                                 | Mach\n" +
    "0     0     0.0                     | iYsym  iZsym  Zsym\n"+
    "%f     %f     %f   | Sref   Cref   Bref\n" %(area, mac, b)+
    "0.00000     0.00000     0.00000   | Xref   Yref   Zref\n"+
    "0.00                               | CDp  (optional)\n"+
    "SURFACE                      | (keyword)\n"+
    "Main Wing\n"+
    "11        1.0\n"+
    "INDEX                        | (keyword)\n"+
    "1814                         | Lsurf\n"+
    "YDUPLICATE\n"+
    "0.0\n"+
    "SCALE\n"+
    "1.0  1.0  1.0\n"+
    "TRANSLATE\n"+
    "0.0  0.0  0.0\n"+
    "ANGLE\n"+
    "0.000                         | dAinc\n"+
    "SECTION                                              |  (keyword)\n"+
    "0.0000    0.0000    0.0000    %f   0.000    8    3   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %(chord_1)+
    "AFIL 0.0 1.0\n"+
    "airfoil.dat\n"+
    "SECTION                                                     |  (keyword)\n" +
    "%f    %f    0.0000    %f   0.000    8    3   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %(offset_1, env_1, chord_2)+
    "AFIL 0.0 1.0\n"+
    "airfoil.dat\n"+
    "SECTION                                                     |  (keyword)\n" +
    "%f   %f    0.0000    %f   0.000   13    1   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %(offset_2, env_2, chord_3)+
    "AFIL 0.0 1.0\n"+
    "airfoil.dat \n" +
    "SECTION                                                     |  (keyword)\n" +
    "%f    %f    0.0000    %f   0.000   13    1   | Xle Yle Zle   Chord Ainc   [ Nspan Sspace ]\n" %(offset_3, env_3, chord_4)+
    "AFIL 0.0 1.0\n"+
    "airfoil.dat \n")
    o.close()

def commands (index):
    commands  = open("comandos.txt" , "w")
    commands.write(" load asa%d\n" %index +
    "oper\n" +
    "a\n" +
    "a 13.5\n" +
    "x\n" +
    "ft\n" +
    "resultado%d.txt\n" %index +
    "quit\n")
    commands.close()

def deletador():
    delete = 1 
    while True:
        if delete == 1:
            dirList = os.listdir()
            arquivo = ""
            for file in dirList:
                if file[-4:] == ".txt":
                    arquivo = file[:-4]
                    os.remove(arquivo + ".txt")
                # if file[-4:] == ".avl":
                #     arquivo = file[:-4]
                #     os.remove(arquivo + ".avl")
            break
        elif delete == 0 :
            break
        else:
            print ("errado")

def criar_asas (contador):

    # Wingspans
    env_1 = random(0.33,0.52)
    env_2 = random(0.33,0.52) + env_1
    env_3 = random(0.33,0.52) + env_2
    # Chords
    chord_1 = random(0.3, 0.4)
    chord_2 = random(chord_1-0.05, chord_1)
    chord_3 = random(chord_2 - 0.05, chord_2)
    chord_4 = random(chord_3 - 0.05, chord_3)
    # Offsets 
    offset_1 = random(0.01, 0.03)
    offset_2 = random(0.01, 0.03) + offset_1
    offset_3 = random(0.01, 0.03) + offset_2

    # Calculations
    area = ((chord_1 + chord_2)*env_1)/2 + ((chord_2 + chord_3)*env_2)/2 + ((chord_3 + chord_4)*env_3)/2
    b = env_3  * 2
    AR = b**2/area
    afilamento = chord_4/chord_1
    mac =  (2*chord_1/3)*((1+afilamento+afilamento**2)/(1+afilamento))

    data = [contador, area, mac, b, chord_1, offset_1, env_1, chord_2, offset_2, env_2, chord_3, offset_3, env_3, chord_4]
    file_creator(data)
    commands (contador)
    run_avl_command = 'avl.exe<' + 'comandos.txt'
    os.system(run_avl_command)

def calculo_mtow (i):
    results = (open("resultado%d.txt" %i)).readlines()
    variables = []
    coefficients = []
    for line in results:
        matches = re.findall("\d\.\d\d\d\d\d", line)
        for value in matches:
            coefficients.append(float(value))

    data = (open("asa%d.avl" %i)).readlines()
    for line in data:
        matches = re.findall("\d\.\d\d\d\d\d\d", line)
        if len(matches) > 0:
            for value in matches:
                variables.append(float(value))

    # Variables structure: [area, mac, envergadura, v_chord_1_p1, v_offset_1_p1, v_env_1_p1, v_chord_2_p1,  v_offset_2_p1, v_env_2_p1, v_chord_3_p1,  v_offset_3_p1, v_env_3_p1, v_chord_4_p1]
    g= 9.81
    rho = 0.993798
    S = variables[0]
    mi = 0.025
    T = 38.125

    passo = 270
    limite = 30
    pista_total = 50

    for k in range (0, passo):
        W= k/(passo/limite) * g
        V = math.sqrt((2*W)/(rho*S*coefficients[-7])) * 1.2 * 0.7
        D = rho*V**(2)*0.5*coefficients[-6]*S
        L = rho*V**(2)*0.5*coefficients[-7]*S
        Slo = round((1.44*(W)**(2))/(g*rho*S*coefficients[-7]*(T-(D+mi*(W-L)))), 2)
        if Slo > pista_total:
            break    
    fator_corretivo = 1.09
    W = ((W/g)/fator_corretivo)
    massa_vazia = (11.48*((S)**2)) - 26.55*(S) + 19.44
    carga_paga = (W - massa_vazia) # Empirical
    pontuacao = 8.3 * 2.7182818 ** (carga_paga/6)

    o  = open("pista%d.txt" %i , "w")
    o.write(str(W) +"\n")
    o.write(str(pontuacao)+"\n")
    o.write(str(carga_paga)+"\n")
    o.close()

    results = [ W, carga_paga, S, variables[2] , variables[1] , coefficients[-7] , coefficients[-6] , pontuacao]
    return results

def gerador_lista(i):
    lista_interna = []
    lista_interna.append (i)

    pistas = (open("pista%d.txt" %i)).readlines()
    lista_interna.extend((float(pistas[0]), float(pistas[2])))

    data = (open("asa%d.avl" %i)).readlines()
    variables = []
    for line in data:
        matches = re.findall("\d\.\d\d\d\d\d\d", line)
        if len(matches) > 0:
            for value in matches:
                variables.append(float(value))
    lista_interna.extend((variables[0], variables[2], variables[1]))

    results = (open("resultado%d.txt" %i)).readlines()
    variables = []
    for line in results:
        matches = re.findall("\d\.\d\d\d\d\d", line)
        for value in matches:
            variables.append(float(value))
    lista_interna.extend((variables[-7], variables[-6], float(pistas[1])))

    return lista_interna

def combinador(lista, indice,i ):
    p_1_i = (lista[i-1][0])
    p_2_i = (lista[len(lista) -i][0] )

    # Abre o arquivo dos pais da asa a ser gerada.
    p_1 = (open("asa%d.avl" %p_1_i)).readlines()
    p_2 = (open("asa%d.avl" %p_2_i)).readlines()
    pais = [p_1, p_2]
    
    variables = []
    for pai in pais:
        pai_variables = []
        for linha in pai:
            matches = re.findall("\d\.\d\d\d\d\d\d", linha)
            if len(matches) > 0:
                for value in matches:
                    pai_variables.append(float(value))
        variables.append(pai_variables)

    # Variables structure: [area, mac, envergadura, v_chord_1_p1, v_offset_1_p1, v_env_1_p1, v_chord_2_p1,  v_offset_2_p1, v_env_2_p1, v_chord_3_p1,  v_offset_3_p1, v_env_3_p1, v_chord_4_p1]

    # Chord Calculations
    ponto_de_corte_corda = 6
    ponto_de_mutacao = -2
    cordas = []
    for i in range (0,4):
        number = 3
        chord_1_f = float("0." + str(int((str(bin(int(str(variables[0][number])[2:8])))[2:ponto_de_corte_corda]) + (str(bin(int(str(variables[1][number])[2:8])))[ponto_de_corte_corda:]), 2)))
        chord_1_f_m = list(str(bin(int(str(chord_1_f)[2:])))[2:])
        if (random(0.0,1.0) < 0.1):
            chord_1_f_m[ponto_de_mutacao] = "1"
        chord_1_f = float("0." + str((int("".join(chord_1_f_m), 2))))
        number += 3
        cordas.append(chord_1_f)
    cordas = sorted(cordas)
    if (cordas[0] > 0.37):
        while (cordas[0] > 0.37):
            cordas[0] = cordas[0]*0.991
            cordas = sorted(cordas)
    if (cordas[3]/cordas[0] >= 0.4):
        while (cordas[3]/cordas[0] >= 0.4):
            cordas[3] = cordas[3]*0.991
    else:
        while (cordas[3]/cordas[0] < 0.3):
            cordas[3] = cordas[3]*1.05
    cordas = sorted(cordas)   

    # Wingspan calculations
    env_1_f = float("0." + str(int((str(bin(int(str(variables[0][5])[2:8])))[2:ponto_de_corte_corda]) + (str(bin(int(str(variables[1][5])[2:8])))[ponto_de_corte_corda:]), 2)))
    env_1_f_m = list(str(bin(int(str(env_1_f)[2:])))[2:])
    if (random(0.0,1.0) < 0.1):
        env_1_f_m[ponto_de_mutacao] = "1"
    env_1_f = float("0." + str((int("".join(env_1_f_m), 2))))
    env_2_f = float("0." + str(int((str(bin(int(str(variables[0][8] - variables[0][5])[2:8])))[2:ponto_de_corte_corda]) + (str(bin(int(str(variables[1][8] - variables[1][5])[2:8])))[ponto_de_corte_corda:]), 2)))
    env_2_f_m = list(str(bin(int(str(env_2_f)[2:])))[2:])
    if (random(0.0,1.0) < 0.1):
        env_2_f_m[ponto_de_mutacao] = "1"
    env_2_f = float("0." + str((int("".join(env_2_f_m), 2)))) + env_1_f
    env_3_f = float("0." + str(int((str(bin(int(str(variables[0][11] - variables[0][8])[2:8])))[2:ponto_de_corte_corda]) + (str(bin(int(str(variables[1][11] - variables[1][8])[2:8])))[ponto_de_corte_corda:]), 2)))
    env_3_f_m = list(str(bin(int(str(env_3_f)[2:])))[2:])
    if (random(0.0,1.0) < 0.1):
        env_3_f_m[ponto_de_mutacao] = "1"
    env_3_f = float("0." + str((int("".join(env_2_f_m), 2)))) + env_2_f
    limite_envergadura = 2.1
    if (env_3_f >= limite_envergadura):
        while (env_3_f >= limite_envergadura):
            env_1_f, env_2_f, env_3_f  = env_1_f * 0.999, env_2_f * 0.999, env_3_f * 0.999

    # Offset calculations
    if (random(0.0,1.0) < 0.5):
        mutador = random(0.95,1.05)
        offset_1_f = variables[0][4] * mutador
        offset_2_f = variables[0][7] * mutador
        offset_3_f = variables[0][10] * mutador
    else:
        mutador = random(0.95,1.05)
        offset_1_f = variables[1][4] * mutador
        offset_2_f = variables[1][7] * mutador
        offset_3_f = variables[1][10] * mutador
    if (offset_3_f< (cordas[1] - cordas[0])/2):
        while (offset_3_f< (cordas[1] - cordas[0])/2):
            offset_3_f = offset_3_f* 1.01
    offset_3_f = offset_3_f + offset_2_f

    # Cálculo de caracteristicas da asa
    area_f = ((cordas[3] + cordas[2])*env_1_f)/2 + ((cordas[2] + cordas[1])*env_2_f)/2 + ((cordas[1] + cordas[0])*env_3_f)/2
    b_f = env_3_f  * 2
    AR = b_f**2/area_f
    afilamento = cordas[0]/cordas[3]
    mac_f =  (2*cordas[3]/3)*((1+afilamento+afilamento**2)/(1+afilamento))

    data = [indice, area_f, mac_f, b_f, cordas[3], offset_1_f, env_1_f, cordas[2], offset_2_f, env_2_f, cordas[1], offset_3_f, env_3_f, cordas[0]]
    file_creator(data)

def atualizador(ciclos, indice, lista):
    # Essa funçao atualiza a lista criada em gerador_relatorio, os filhos são adicionados agora e um arquivo txt é gerado.
    indice_real = indice
    for i in range (1, ciclos):
        indice_real += 1
        commands(indice_real)
        run_avl_command = 'avl.exe<' + 'comandos.txt'
        os.system(run_avl_command)
        results = calculo_mtow(indice_real)
        identificador = [indice_real]
        filho = identificador + results
        lista.append(filho)
        lista_pronta = sorted(lista, key=itemgetter(8), reverse=True)
    return lista_pronta
    
def gerador_relatorio(lista_pronta):
    file = open ("Resultados.md", "w")
    file.write("|Wing |   MTOW(Kg) | Payload | Area |  Wingspan | Mean Chord |   CL   |   CD   |   Score   |  \n"+
               "---------------------------------------------------------------------------------------------------------\n")
    for i in range (len(lista_pronta)):

        file.write("%d         %6.2f   %6.2f      %5.3f    %5.3f      %5.3f      %5.3f   %6.4f    %5.3f\n" %(lista_pronta[i][0], lista_pronta[i][1], lista_pronta[i][2], lista_pronta[i][3], lista_pronta[i][4],lista_pronta[i][5], lista_pronta[i][6],lista_pronta[i][7], lista_pronta[i][8]))
    file.close

def adicionador (interna, completa):
    # Adiciona o melhor da geracao
    sorteada = sorted(interna, key=itemgetter(8), reverse=True)
    melhor = sorteada[0]
    completa.append(melhor)

def visualizador (lista):
    indices = []
    lista_corrigida = []
    size = []
    index = 1
    lista  = lista #list (dict.fromkeys(lista))

    # Limite inferior pra plotar
    for i in range (0, len(lista)):
        if (lista[i][8] > 5.0):
            lista_corrigida.append(lista[i][8])
            size.append(lista[i][4])

    # Impedir um inferior que anterior (diferenca menor que 0)
    while index < len(lista_corrigida):
        if lista_corrigida[index] - lista_corrigida[index - 1] < 0:
            del lista_corrigida[index]
            del size[index]
        else:
            index += 1
    # Criar indice pra numerar geracao
    for i in range (1, len(lista_corrigida)+1):
        indices.append(i)
    
    # Salvar os valors em um .csv
    colnames=['Geração', 'Pontuação', 'Envergadura'] 
    resultados = pd.DataFrame(zip(indices,lista_corrigida, size), columns  = colnames)
    resultados.to_csv('Gráfico %d.csv' %(len(indices)-1),index=False)

    # Criar o gráfico
    plt.style.use('seaborn')
    plt.scatter(indices,lista_corrigida, s=60, c = size, cmap = 'Greens', edgecolor= "black", linewidth = 1, alpha = 1)
    cbar = plt.colorbar()
    cbar.set_label ('Envergadura')
    plt.title ("Asas")
    plt.xlabel("Geração")
    plt.ylabel("Pontuação")
    plt.tight_layout()
    z = np.polyfit(indices, lista_corrigida, 1)
    p = np.poly1d(z)
    plt.plot(indices,p(indices),"r--")
    plt.show()

def main():
    final = []
    # Parameters
    qntd_asas = int(input("How many generations: ")) + 1
    zyklus = qntd_asas
    limite_populacional = qntd_asas
    lista = []
    # Criacao da populacao inicial
    for i in range (1,qntd_asas):
        criar_asas(i)
        calculo_mtow(i)
        listinha = gerador_lista(i)
        lista.append(listinha)
        dirList = os.listdir()
        for i in range (i, qntd_asas):
            for file in dirList:
                if file == "pista%d.txt" %i:
                    os.remove ("pista%d.txt" %i)
    adicionador (lista, final)
    # Combinacoes
    for i in range (1, zyklus):
        ciclos = (int(round((len(lista))/2))) + 1
        indice = len (lista)
        for i in range (1,ciclos):
            indice += 1
            combinador(lista, indice, i)
        indice = len (lista)
        lista = atualizador(ciclos, indice, lista)
        adicionador (lista, final)
        # Deletar os extras acima do limite populacional
        if len(lista) > limite_populacional:
            dirList = os.listdir()
            deletados= []
            for i in range (limite_populacional, len(lista)-1):
                deletados.append(lista[limite_populacional][0])
                del lista[limite_populacional]
            # Varre todos os arquivos da pasta para checar se for uma asa p ser deletada e deleta.
            for i in range (0, len(deletados)):
                for file in dirList:
                    if file == "asa%d.avl" %(deletados[i]):
                        os.remove ("asa%d.avl" %(deletados[i]))
                        os.remove ("resultado%d.txt" %(deletados[i]))
            # Renomar as asas restantes
            for i in range (1, limite_populacional + 2):
                os.rename ("asa%d.avl"%lista[i-1][0], "asan%d.avl"%i )
                os.rename ("resultado%d.txt"%lista[i-1][0], "resultadon%d.txt"%i )
            for i in range (1, limite_populacional + 2):
                os.rename ("asan%d.avl"%i, "asa%d.avl"%i)
                os.rename ("resultadon%d.txt"%i, "resultado%d.txt"%i )
                lista[i-1][0] =  i
    gerador_relatorio(lista)
    visualizador (final)
    deletador()

main()
