import copy
import time
import os
import math
import itertools

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
    algorithm = input("BF\nDF\nDFI\nUCS\nA-start\nIDA\nGreedy\nSelectati algoritmul: ")
    # algorithm = 'bf'


    if algorithm.lower()== 'bf':
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            breadth_first(gr, nrSolutiiCautate=nsol)
    if algorithm.lower() == 'dfi':
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            depth_first_iterativ(gr, nrSolutiiCautate=nsol)
    if algorithm.lower() == 'df':
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            depth_first(gr, nrSolutiiCautate=nsol)
    if algorithm.upper() == 'UCS':
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            uniform_cost(gr, nrSolutiiCautate=nsol)


    # TO DO repara a_star
    if algorithm.lower() == 'a_star':
        cod_euristica = int(input(
            "1.Euristica banala\n2.Euristica admisibila 1\n3.Euristica admisibila 2\n4.Euristica neadmisibila\nSelectati euristica: "))
        euristica = ''
        if cod_euristica == 1:
            euristica = 'euristica banala'
        if cod_euristica == 2:
            euristica = 'euristica admisibila 1'
        if cod_euristica == 3:
            euristica = 'euristica admisibila 2'
        if cod_euristica == 4:
            euristica = 'euristica neadmisibila'
        if cod_euristica not in [1, 2, 3, 4]:
            print("Alegeti o varianta din lista de mai sus!")
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            a_star(gr, nrSolutiiCautate=nsol, tip_euristica=euristica)
        if algorithm.upper() == 'IDA':
            cod_euristica = int(input(
                "1.Euristica banala\n2.Euristica admisibila 1\n3.Euristica admisibila 2\n4.Euristica neadmisibila\nSelectati euristica: "))
            euristica = ''
            if cod_euristica == 1:
                euristica = 'euristica banala'
            if cod_euristica == 2:
                euristica = 'euristica admisibila 1'
            if cod_euristica == 3:
                euristica = 'euristica admisibila 2'
            if cod_euristica == 4:
                euristica = 'euristica neadmisibila'
            if cod_euristica not in [1, 2, 3, 4]:
                print("Alegeti o varianta din lista de mai sus!")
            for file in input_files:
                gr = Graph(file, output_director, timeout)
                NodParcurgere.gr = gr
                # ida_star(gr, nrSolutiiCautate=nsol, tip_euristica=euristica)
    if algorithm.lower() == 'greedy':
        cod_euristica = int(input(
            "1.Euristica banala\n2.Euristica admisibila 1\n3.Euristica admisibila 2\n4.Euristica neadmisibila\nSelectati euristica: "))
        euristica = ''
        if cod_euristica == 1:
            euristica = 'euristica banala'
        if cod_euristica == 2:
            euristica = 'euristica admisibila 1'
        if cod_euristica == 3:
            euristica = 'euristica admisibila 2'
        if cod_euristica == 4:
            euristica = 'euristica neadmisibila'
        if cod_euristica not in [1, 2, 3, 4]:
            print("Alegeti o varianta din lista de mai sus!")
        for file in input_files:
            gr = Graph(file, output_director, timeout)
            NodParcurgere.gr = gr
            greedy(gr, nrSolutiiCautate=nsol, tip_euristica=euristica)
    # if algorithm not in ['bf', 'df', 'dfi', 'ucs', 'a-star', "greedy"]:
    #     print("Alegeti o varianta din lista de mai sus!")

# Diferenta dintre 2 liste
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
    def afisDrum(self, algorithm,output_dir, input_file, afisCost= False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        output_file = 'output_' + algorithm + '_' + os.path.split(input_file)[1]
        f = open(os.path.join(output_dir, output_file), "a")
        i = 1
        for nod in l:

            if nod.parinte is not None:
                if nod.parinte.info[2] == 1:
                    mbarca1 = self.__class__.gr.malInitial
                    mbarca2 = self.__class__.gr.malFinal
                else:
                    mbarca1 = self.__class__.gr.malFinal
                    mbarca2 = self.__class__.gr.malInitial
                f.write(str(i) + '. ' + str(nod) + '\n')
                i += 1
        if afisCost:
            f.write("\nCost: " +str(self.g))
        if afisLung:
            f.write("\nLungime: " + str(len(l)) )
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
        # Adaugam nrNoduri pentru a folosi la DFI
        self.nrNoduri = 100

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

        # if self.__class__.malInitial == self.__class__.malFinal:
        #     functieDeEroare(self, in_dir, out_dir)
        #
        # elif max(self.__class__.cannibals) > self.__class__.GMAX or max(self.__class__.missionaries):
        #     functieDeEroare2(self,in_dir, out_dir)

        # if self.__class__.malFinal != self.__class__.malInitial:
        self.start = (self.__class__.missionaries, self.__class__.cannibals, 1)  # informatia nodului de start

    def testeaza_scop(self, nodCurent):
        return len(nodCurent.info[0]) == len(nodCurent.info[1]) == nodCurent.info[2] == 0 or self.__class__.malInitial == self.__class__.malFinal

    def functieDeEroare(self, nodCurent):
        return self.__class__.GMAX < max(self.__class__.missionaries) or self.__class__.GMAX < max(self.__class__.cannibals)

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
                                              h=self.calculeaza_h(infoNodNou, tip_euristica)))
        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica='euristica banala'):
        if tip_euristica == "euristica banala":
            if not len(infoNod[0])==len(infoNod[1])==infoNod[2]==0:
                return 1
            return 0

        elif tip_euristica == 'euristica admisibila 1':
            if infoNod[0]:
                mis = min(infoNod[0])
            else:
                mis =1
            if infoNod[1]:
                can = min(infoNod[1])
            else:
                can =1

            return (sum(infoNod[0])+sum(infoNod[1]))/(mis+can)

        elif tip_euristica == 'euristica admisibila 2':
            if infoNod[0]:
                mis = min(infoNod[0])
            else:
                mis =1
            if infoNod[1]:
                can = min(infoNod[1])
            else:
                can =1
            return min(mis, can)
        else:
            # Euristica neadmisibila
            suma = sum(infoNod[0] + sum(infoNod[1])) * 100

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
                output_file = 'output_' + 'breath_first' + '_' + os.path.split(gr.input_dir)[1]
                f = open(os.path.join(gr.output, output_file), "a")


                length, f = nodCurent.afisDrum( algorithm='breath_first', output_dir=gr.output, input_file=gr.input_dir, afisCost=True,
                             afisLung=True)
                f.write("\nNod numar: " + str(index) + '\n')
                # f.write("Lungime " + str(length) + '\n')
                finish_time = time.time()
                f.write("Timp solutie: " + str(round(1000 * (finish_time - start_time_for_solution))) + "ms" + '\n')
                start_time_for_solution = time.time()
                f.write("\n--------------------------------------------------------------------------------------\n")
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    f.write("Noduri total expandate: " + str(total_number_of_nodes) + '\n')
                    f.write("Noduri maxim noduri expandate: " + str(max_nodes) + '\n')
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent)
            total_number_of_nodes += len(lSuccesori)
            if max_nodes < len(lSuccesori) + len(c):
                max_nodes = len(lSuccesori) + len(c)
            c.extend(lSuccesori)

def depth_first(gr, nrSolutiiCautate):
    total_number_of_nodes = 0
    max_nodes = 0
    index = 0
    start_time_for_solution = time.time()
    df(gr, NodParcurgere(gr.start, None), nrSolutiiCautate, total_number_of_nodes, max_nodes,
       start_time_for_solution, index)
def df(gr, nodCurent, nrSolutiiCautate, total_number_of_nodes, max_nodes, start_time_for_solution, index):
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    index += 1
    time_spent = time.time()
    if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
        print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)
        return
    if gr.functieDeEroare(nodCurent):
        output_file = 'output_' + 'depth_first' + '_' + os.path.split(gr.input_dir)[1]
        f = open(os.path.join(gr.output, output_file), "a")
        f.write(" NU EXISTA SOLUTIE :Exista persoane care nu incap in barca")


    elif gr.testeaza_scop(nodCurent):
        finish_time = time.time()
        if round(1000 * (finish_time - start_time_for_solution)) == 0:
            output_file = 'output_' + 'df' + '_' + os.path.split(gr.input_dir)[1]
            f = open(os.path.join(gr.output, output_file), "a")
            f.write('Malul initial coincide cu cel final')
            print()
        else:
            length, f = nodCurent.afisDrum(algorithm='DF', output_dir=gr.output, input_file=gr.input_dir)
            f.write("Nod numar: " + str(index) + '\n')
            f.write("Timp solutie: " + str(round(1000 * (finish_time - start_time_for_solution))) + "ms" + '\n')
            start_time_for_solution = time.time()
            f.write("\n-----------------------------------------------------------------------------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                f.write("Noduri total expandate: " + str(total_number_of_nodes) + '\n')
                f.write("Noduri maxim noduri expandate: " + str(max_nodes) + '\n')
                return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    total_number_of_nodes += len(lSuccesori)
    if max_nodes < len(lSuccesori):
        max_nodes = len(lSuccesori)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(gr, sc, nrSolutiiCautate, total_number_of_nodes, max_nodes, start_time_for_solution,
                                  index)

    return nrSolutiiCautate

def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start,None, 0, gr.calculeaza_h(gr.start))]
    total_number_of_nodes = 0
    max_nodes = 0
    start_time_for_solution = time.time()
    index = 0
    while len(c) > 0:
        index += 1
        time_spent = time.time()
        if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
            print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)
            return
        nodCurent = c.pop(0)

        if gr.functieDeEroare(nodCurent):
            output_file = 'output_' + 'a_star' + '_' + os.path.split(gr.input_dir)[1]
            f = open(os.path.join(gr.output, output_file), "a")
            f.write(" NU EXISTA SOLUTIE :Exista persoane care nu incap in barca")
            break

        if gr.testeaza_scop(nodCurent):
            length, f = nodCurent.afisDrum(algorithm='UCS', output_dir=gr.output, input_file=gr.input_dir)
            f.write("Nod numar " + str(index) + '\n')
            finish_time=time.time()
            f.write("Timp solutie: " + str(round(1000 * (finish_time - start_time_for_solution))) + "ms" + '\n')
            start_time_for_solution = time.time()
            f.write("\n-------------------------------------------------------------------------------------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                f.write("Noduri total expandate: " + str(total_number_of_nodes) + '\n')
                f.write("Noduri maxim noduri expandate: " + str(max_nodes) + '\n')
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        total_number_of_nodes += len(lSuccesori)
        if max_nodes < len(lSuccesori) + len(c):
            max_nodes = len(lSuccesori) + len(c)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)



def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    total_number_of_nodes = 0
    max_nodes = 0
    index = 0
    start_time_for_solution = time.time()
    while len(c) > 0:
        nodCurent = c.pop(0)
        if gr.functieDeEroare(nodCurent):
            output_file = 'output_' + 'a_star' + '_' + os.path.split(gr.input_dir)[1]
            f = open(os.path.join(gr.output, output_file), "a")
            f.write(" NU EXISTA SOLUTIE :Exista persoane care nu incap in barca")
            break

        index += 1
        time_spent = time.time()
        if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
            print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)
            return

        if gr.testeaza_scop(nodCurent):
            length, f = nodCurent.afisDrum( algorithm='a-star', output_dir=gr.output, input_file=gr.input_dir, afisCost=True,
                         afisLung=True)
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



# NU MERGE!!!!!!!
def depth_first_iterativ(gr, nrSolutiiCautate=1):
    for i in range(1, gr.nrNoduri+1):
        if nrSolutiiCautate==0:
            return
        total_number_of_nodes = 0
        max_nodes=0
        index=0
        start_time_for_solution = time.time()
        nrSolutiiCautate = dfi(gr, NodParcurgere(gr.start, None), i, nrSolutiiCautate, total_number_of_nodes, max_nodes, start_time_for_solution, index)

def dfi(gr, nodCurent, adancime, nrSolutiiCautate, total_number_of_nodes, max_nodes, start_time_for_solution, index):
    time_spent = time.time()
    index += 1
    if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
        print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)
        return
    if adancime == 1 and gr.testeaza_scop(nodCurent) and gr.functieDeEroare(nodCurent)==0 and gr.functieDeEroare2(nodCurent):
        length, f = nodCurent.afisDrum(algorithm='DFI', output_dir=gr.output, input_file=gr.input_dir)
        f.write("Nod numar: " + str(index) + '\n')
        finish_time = time.time()
        f.write("Timp solutie: " + str(round(1000 * (finish_time - start_time_for_solution))) + "ms" + '\n')
        start_time_for_solution = time.time()
        f.write("\n-------------------------------------------------------------------------------------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            f.write("Noduri total expandate: " + str(total_number_of_nodes) + '\n')
            f.write("Noduri maxim noduri expandate: " + str(max_nodes) + '\n')
            return nrSolutiiCautate
    elif gr.functieDeEroare(nodCurent):
        output_file = 'output_' + 'a_star' + '_' + os.path.split(gr.input_dir)[1]
        f = open(os.path.join(gr.output, output_file), "a")
        f.write(" NU EXISTA SOLUTIE :Exista persoane care nu incap in barca")
    else:
        output_file = 'output_' + 'a_star' + '_' + os.path.split(gr.input_dir)[1]
        f = open(os.path.join(gr.output, output_file), "a")
        f.write(" Oamenii sunt pe malul dorit")
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        total_number_of_nodes += len(lSuccesori)
        if max_nodes < len(lSuccesori):
            max_nodes = len(lSuccesori)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(gr, sc, adancime - 1, nrSolutiiCautate,
                                       total_number_of_nodes, max_nodes, start_time_for_solution, index)
    return nrSolutiiCautate

# def ida_star(gr, nrSolutiiCautate, tip_euristica):
#     nodStart = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
#     limita = nodStart.f
#     while True:
#
#         print("Limita de pornire: ", limita)
#         nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate)
#         if rez == "gata":
#             break
#         if rez == float('inf'):
#             print("Nu mai exista solutii!")
#             break
#         limita = rez
#         print(">>> Limita noua: ", limita)
#         input()
#
#
# def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate):
#     print("A ajuns la: ", nodCurent)
#     if nodCurent.f > limita:
#         return nrSolutiiCautate, nodCurent.f
#     if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
#         print("Solutie: ")
#         nodCurent.afisDrum()
#         print(limita)
#         print("\n----------------\n")
#         input()
#         nrSolutiiCautate -= 1
#         if nrSolutiiCautate == 0:
#             return 0, "gata"
#     lSuccesori = gr.genereazaSuccesori(nodCurent)
#     minim = float('inf')
#     for s in lSuccesori:
#         nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate)
#         if rez == "gata":
#             return 0, "gata"
#         print("Compara ", rez, " cu ", minim)
#         if rez < minim:
#             minim = rez
#             print("Noul minim: ", minim)
#     return nrSolutiiCautate, minim

def greedy(gr, nrSolutiiCautate, tip_euristica='euristica banala'):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    total_number_of_nodes = 0
    max_nodes = 0
    start_time_for_solution = time.time()
    index = 0
    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        index += 1
        time_spent = time.time()
        if round(1000 * (time_spent - start_time_for_solution)) / 1000 > gr.timeout:
            print("Timpul de executie a depasit timpul introdus pentru fisierul " + gr.nume_fisier_in)
            return
        nodCurent = c.pop(0)


        if gr.functieDeEroare(nodCurent):
            output_file = 'output_' + 'Greedy' + '_' + os.path.split(gr.input_dir)[1]
            f = open(os.path.join(gr.output, output_file), "a")
            f.write(" NU EXISTA SOLUTIE :Exista persoane care nu incap in barca")
            break

        if gr.functieDeEroare2(nodCurent):
            output_file = 'output_' + 'Greedy' + '_' + os.path.split(gr.input_dir)[1]
            f = open(os.path.join(gr.output, output_file), "a")
            f.write(" Barca se afla pe malul care trebuie")
            break

        if gr.testeaza_scop(nodCurent):
            length, f = nodCurent.afisDrum(algorithm='Greedy', output_dir=gr.output, input_file=gr.input_dir)
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
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        total_number_of_nodes += len(lSuccesori)
        if max_nodes < len(lSuccesori) + len(c):
            max_nodes = len(lSuccesori) + len(c)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].h > s.h:
                    gasit_loc = True
                    break
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

