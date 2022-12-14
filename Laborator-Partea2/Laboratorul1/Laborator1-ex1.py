
# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, id, info, parinte):
        self.id =id # este indicele din vectorul de noduri
        self.info =info
        self.parinte =parinte  # parintele din arborele de parcurgere

    def obtineDrum(self):
        l = [self.info];

        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):  # retur  eaza si lungimea drumului
        l=self.obtineDrum()
        print("Solutie :" + ("->").join(l))
        return len(l)


    def contineInDrum(self, infoNodNou):
        nodDrum=self
        while nodDrum is not None:
            if(infoNodNou== nodDrum.info):
                return True
            nodDrum=nodDrum.parinte

        return False

    def __repr__(self):
        sir=" "
        sir+= self.info+" ( "
        sir+= "id = {}, ".format(self.id)
        sir+= "drum="
        drum=self.obtineDrum()
        sir+= ("->").join(drum)
        sir+= ") "
        return(sir)


class Graph:  #  graful problemei
    def __init__(self, noduri, matrice, start, scopuri):
        self.noduri=noduri
        self.matrice=matrice
        self.nrNoduri=len(matrice)
        self.start=start
        self.scopuri=scopuri

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        scopuri = [" f", "j "]
        listaSuccesori=[ ]
        listaSuccesoriPrelucrata= []
        for i in range(self.nrNoduri):
            if self.matrice[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou=NodParcurgere(i, self.noduri[i], nodCurent)
                listaSuccesori.append(nodNou)
                listaSuccesoriPrelucrata.append(nodNou.info)
                # if nodNou.info in scopuri:
                #     print("Lingime solutie: " + str(nodCurent.afisDrum()))
        if (len(listaSuccesori)> 0):
            # print("Genereaza succesori " + str(listaSuccesori))
            # print()
            # print(str(lista2))
            # print()
            print("Se extinde nodul " + str(nodCurent.info))
            print("Se adauga in coada " + str(listaSuccesoriPrelucrata))

        return listaSuccesori

    def __repr__(self):
        sir=" "
        for (k,v) in self.__dict__.items() :
            sir+= "{ } = {}\n".format(k,v)
        return(sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta



def breadth_first(gr):
    global nrSolutiiCautate
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[ NodParcurgere(gr.noduri.index(start), start, None)]
    print(" C: " + str(c))
    continua=True  #  variabila pe care o setez la false cand consider ca s-au afisat suficiente solutii
    while(len(c)>0 and continua):
        print("Coada actuala: " + str(c))
        nodCurent=c. pop(0)

        if nodCurent.info in scopuri:

            print("Lungime solutie: " + str(nodCurent.afisDrum()))
            print()
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0 :
                continua=False
        lSuccesori=gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)
        # print(str(c))






if __name__ == '__main__':
    noduri = ["a ", "b ", "c ", "d ", "e ", "f ", "g ", "h ", "i ", "j "]

    m = [
        [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    ]

    start = "a "
    scopuri = [" f", "j "]
    gr = Graph(noduri, m, start, scopuri)

    #### algoritm BF
    # presupunem ca vrem mai multe solutii (un numar fix)
    # daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
    # si doar oprim algoritmul la afisarea primei solutii
    nrSolutiiCautate = 4
    breadth_first(gr)
