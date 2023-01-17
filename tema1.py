import copy
import time
import os
import sys
import math
import itertools
import numpy
""" 
Citire de la tastura numarul de solutii Cerinta 1. 

"""

def read_nsolutii():
    nsol = 0
    while True:
        try:
            nsol = int(input("Introduceti numarul de solutii dorite: "))
            if nsol < 0:
                print('\033[91m' + "Introduceti un numar de solutii mai mare decat 0!" + '\033[0m')
            else:
                break
        except Exception as e:
            print("Introduceti un numar natural de solutii mai mare decat 0!")

    return nsol

""" 
Citire fisiere input + output cerinta 1.
"""

def read_directors():
    while True:
        input_dir = input("Introduceti numele folderului input: ")
        try:
            dir_list = os.listdir(input_dir)
            break
        except Exception:
            print("Acest folder nu exista, introduceti un nume valid!")

    output_dir = input("Introduceti numele folderului output: ")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        for file in os.listdir(output_dir):
            if not file.endswith(".txt"):
                continue
            os.remove(os.path.join(output_dir, file))

    input_files = []
    for file in dir_list:
        input_files.append(os.path.join(input_dir, file))
    return input_files, output_dir


"""
Citire Timeout cerinta 1.
"""
def read_timeout():
    timeout = 0
    while True:
        try:
            timeout = float(input("Introduceti numarul de secunde de timeout: "))
            if timeout <= 0:
                print("Numarul de secunde trebuie sa fie mai mare decat 0!")
            else:
                break
        except Exception:
            print("Numarul de secunde este natural si mai mare decat 0")

    return timeout

""" 
Alegere algoritm dorit si tip de euristica
"""

def select_algorithm( nsol, timeout):
    input_files, output_director= read_directors()
    # input_files = '\input'
    # output_director= '\out'
    algorithm = input("BF\nDF\nDFI\nUCS\nA*\nGreedy\nSelectati algoritmul: ")
    # algorithm = 'bf'


    if algorithm.lower()== 'bf':
        # print("Solutii obtinute cu BF:")
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            breadth_first(gr, nrSolutiiCautate=nsol)
    # if algorithm.lower() == 'df':
    #     # print("Solutii obtinute cu DF:")
    #     for file in input_files:
    #         gr = Graph(file, output_dir_name, timeout)
    #         depth_first(gr, nrSolutiiCautate=nsol)
    # if algorithm.lower() == 'dfi':
    #     for file in input_files:
    #         gr = Graph(file, output_dir_name, timeout)
    #         depth_first_iterativ(gr, nrSolutiiCautate=nsol)
    # if algorithm == 4:
    #     # print("Solutii obtinute cu UCS:")
    #     for file in input_files:
    #         gr = Graph(file, output_dir_name, timeout)
    #         uniform_cost(gr, nrSolutiiCautate=nsol)
    # if algorithm == 5:
    #     cod_euristica = int(input(
    #         "1.Euristica banala\n2.Euristica admisibila 1\n3.Euristica admisibila 2\n4.Euristica neadmisibila\nSelectati euristica: "))
    #     euristica = ''
    #     if cod_euristica == 1:
    #         euristica = 'euristica banala'
    #     if cod_euristica == 2:
    #         euristica = 'euristica admisibila 1'
    #     if cod_euristica == 3:
    #         euristica = 'euristica admisibila 2'
    #     if cod_euristica == 4:
    #         euristica = 'euristica neadmisibila'
    #     if cod_euristica not in [1, 2, 3, 4]:
    #         print("Alegeti o varianta din lista de mai sus!")
    #     for file in input_files:
    #         gr = Graph(file, output_dir_name, timeout)
    #         a_star(gr=gr, nrSolutiiCautate=nsol, tip_euristica=euristica)
    # if algorithm == 6:
    #     for file in input_files:
    #         gr = Graph(file, output_dir_name, timeout)
    #         uniform_cost(gr, nrSolutiiCautate=nsol)
    # if algorithm not in ['bf', 'df', 'dfi', 'ucs', 'a-star', "greedy"]:
    #     print("Alegeti o varianta din lista de mai sus!")

def difLista(l1, l2):
    l3 = []
    for l in l1:
        if l not in l2:
            l3.append(l)
    return l3



# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l



    # TO DO : continuat afisaz
    def afisDrum(self, algorithm,output_dir, input_file, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        output_file = 'output_' + algorithm + '_' + os.path.split(input_file)[1]
        f = open(os.path.join(output_dir, output_file), "a")
        for nod in l:
            if nod.parinte is not None:
                if nod.parinte.info[2] == 1:
                    mbarca1 = self.__class__.gr.malInitial
                    mbarca2 = self.__class__.gr.malFinal
                else:
                    mbarca1 = self.__class__.gr.malFinal
                    mbarca2 = self.__class__.gr.malInitial
                print(
                    ">>> Barca s-a deplasat de la malul {} la malul {} cu {} canibali si {} misionari.".format(mbarca1,
                                                                                                               mbarca2,
                                                                                                               difLista(
                                                                                                                   nod.info[
                                                                                                                       0],
                                                                                                                   nod.parinte.info[
                                                                                                                       0]),

                                                                                                                   difLista(nod.info[
                                                                                                                       1] ,nod.parinte.info[
                                                                                                                       1])))
                f.write("\n>>> Barca s-a deplasat de la malul {} la malul {} cu {} canibali si {} misionari.".format(mbarca1,
                                                                                                               mbarca2,
                                                                                                               difLista(
                                                                                                                   nod.info[
                                                                                                                       0],
                                                                                                                   nod.parinte.info[
                                                                                                                       0]),

                                                                                                                   difLista(nod.info[
                                                                                                                       1] ,nod.parinte.info[
                                                                                                                       1])))
            # print()
            print(str(nod))
            f.write(str(nod))
        if afisCost:
            print("Cost: ", self.g)
            f.write("\nCost:" + str(self.g) + '\n')
        print("--------------------------------------------------------------------------")
        return len(l), f

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        if self.info[2] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"
        return (
                "Mal: " + self.gr.malInitial + " Canibali: {} Misionari: {} {}  |||  Mal:" + self.gr.malFinal + " Canibali: {} Misionari: {} {}").format(
            self.info[1], self.info[0], barcaMalInitial, difLista(self.__class__.gr.cannibals ,self.info[1]),
                                                         difLista(self.__class__.gr.missionaries, self.info[0]), barcaMalFinal)





class Graph:  # graful problemei
    def __init__(self, in_dir, out_dir, timeout):

        def stiva(sir):
            lista = []
            weights = sir.split(' ')
            for weight in weights:
                lista.append(int(weight))
            return lista

        # Setare timeout si fisiere
        self.timeout=timeout
        self.input_dir=in_dir
        self.f=open(in_dir, 'r')
        self.output=out_dir

        # Citire date
        datas=self.f.read()
        print(datas)
        datas =  datas.split('\n')

        # self.__class__ inseamna clasa curenta
        self.__class__.N = int(datas[0].split('=')[1])
        print(self.N)
        self.__class__.missionaries=stiva(datas[1])
        self.__class__.cannibals=stiva(datas[2])
        self.__class__.M= int(datas[3].split('=')[1])
        # print(self.M)

        self.__class__.GMAX =int(datas[4].split('=')[1])
        self.__class__.malInitial = datas[5].split('=')[1]
        self.__class__.malFinal = datas[6].split('=')[1]

        self.start = (self.__class__.missionaries, self.__class__.cannibals, 1)  # informatia nodului de start

    def testeaza_scop(self, nodCurent):
        return len(nodCurent.info[0]) == len(nodCurent.info[1]) == nodCurent.info[2] == 0


    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        # mal curent = mal cu barca; mal opus=mal fara barca
        def test_conditie(mis, can):
            return len(mis) == 0 or len(mis) >= len(can)

        def difLista(l1, l2):
            l3 = []
            for l in l1:
                if l not in l2:
                    l3.append(l)
            return l3


        listaSuccesori = []
        barca = nodCurent.info[2]
        # nodCurent.info va va contine un triplet format din (can, mis, mal_barca), can, mis = liste
        if barca == 1:
            misMalCurent = copy.deepcopy(nodCurent.info[0]) # Ok
            canMalCurent = copy.deepcopy(nodCurent.info[1])# Ok
            canMalOpus = difLista(Graph.cannibals, canMalCurent)
            misMalOpus = difLista(Graph.missionaries, misMalCurent)

        else:  # barca==0 adica malul final
            canMalOpus = copy.deepcopy(nodCurent.info[1]) # malul opus (barcii) este cel initial
            misMalOpus = copy.deepcopy(nodCurent.info[0])
            canMalCurent = difLista(Graph.cannibals,canMalOpus)
            misMalCurent = difLista(Graph.missionaries, misMalOpus)

        maxMisionariBarca = min(Graph.N, Graph.M)
        for i in range (maxMisionariBarca+1):
            misSubmultimi=list(itertools.combinations(misMalCurent,i))
            for misBarca in misSubmultimi: # Parcurgere submultimi
                misBarca = list(misBarca)
                if len(misBarca) == 0:
                    nrMaxCan = min(Graph.M, len(canMalCurent))
                    nrMinCan = 1
                else:
                    nrMaxCan = min (Graph.M-len(misBarca), len(canMalCurent))
                    nrMinCan = 0
                for nrCan in range (nrMinCan, nrMaxCan + 1):
                    canSubmultimi = list(itertools.combinations(canMalCurent, nrCan))
                    for canBarca in canSubmultimi:
                        canBarca = list(canBarca)

                        misMalCurentNou = difLista(misMalCurent,misBarca)
                        canMalCurentNou = difLista(canMalCurent , canBarca)
                        misMalOpusNou = misMalOpus + misBarca
                        canMalOpusNou = canMalOpus + canBarca


                        if not test_conditie(misMalCurentNou, canMalCurentNou):
                            continue

                        if not test_conditie(misMalOpusNou, canMalOpusNou):
                            continue


                        if sum(canBarca)+sum(misBarca) > Graph.GMAX:
                            continue

                        if len(canBarca) + len(misBarca) > Graph.M:
                            continue

                        if barca == 1:
                            infoNodNou = ( misMalCurentNou,canMalCurentNou, 0)

                        else:
                            infoNodNou = ( misMalOpusNou,canMalOpusNou, 1)

                        if not nodCurent.contineInDrum(infoNodNou):
                            costSuccesor = sum(canBarca)+ sum(misBarca)
                            listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor,
                                              h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))
        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica='euristica_banala'):
        if tip_euristica == "euristica banala":
            if not infoNod[0]==infoNod[1]==infoNod[2]:
                return 1
            return 0
        elif tip_euristica == 'euristica admisibila 1':
            # return 2 * math.ceil((len(infoNod[0]) + len(infoNod[1])) / (self.M - 1)) + (1 - infoNod[2]) - 1
            return 0
        elif tip_euristica == 'euristica admisibila 2':
            mis = infoNod.info[0]
            can = infoNod.info[1]
            suma = sum(mis) + sum(can)
            return sum
        else:
            # Euristica neadmisibila
            suma = 0
            mis = infoNod.info[0]
            can = infoNod.info[1]
            suma -= sum(mis) + sum(can)

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]
    total_number_of_nodes = 0
    max_nodes = 0
    start_time_for_solution = time.time()
    index = 0
    while len(c) > 0:
        # print("Coada actuala: " + str(c))

        index += 1
        time_spent = time.time()
        if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
            print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)

        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent):
            print("Solutie:")

            #  in_dir, out_dir
            length, f = nodCurent.afisDrum( algorithm='bf', output_dir=gr.output, input_file=gr.input_dir, afisCost=False,
                         afisLung=False)
            f.write("\nNod numar: " + str(index) + '\n')
            finish_time = time.time()

            f.write("Timp solutie: " + str(round(1000 * (finish_time - start_time_for_solution))) + "ms" + '\n')
            start_time_for_solution = time.time()
            f.write("\n--------------------------------------------------------------------------------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)

def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    total_number_of_nodes = 0
    max_nodes = 0
    index = 0
    start_time_for_solution = time.time()
    while len(c) > 0:
        nodCurent = c.pop(0)
        index += 1
        time_spent = time.time()
        if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
            print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)
            return

        if gr.testeaza_scop(nodCurent):
            length, f = nodCurent.afisDrum( algorithm='a-start', output_dir=gr.output_director, input_file=gr.input_file, afisCost=False,
                         afisLung=False)
            f.write("Nod numar: " + str(index) + '\n')
            finish_time = time.time()
            f.write("Timp solutie: " + str(round(1000 * (finish_time - start_time_for_solution))) + "ms" + '\n')
            start_time_for_solution = time.time()
            f.write("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                f.write("Noduri total expandate: " + str(total_number_of_nodes) + '\n')
                f.write("Noduri maxim noduri expandate: " + str(max_nodes) + '\n')
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        total_number_of_nodes += len(lSuccesori)
        if max_nodes < len(lSuccesori) + len(c):
            max_nodes = len(lSuccesori) + len(c)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

if __name__ == '__main__':
    # nsol = read_nsolutii()
    nsol = 3 # Harcodat
    #timeout=read_timeout()
    timeout=1000000000 # Harcodat
    # select_algorithm(input, output, nsol, timeout)
    select_algorithm( nsol, timeout)

