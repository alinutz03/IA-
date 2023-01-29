import math
import sys
import time
import pygame
import copy

def elem_identice(lista):
	if(len(set(lista))==1) :
		return lista[0] if lista[0]!=Joc.GOL else False
	return False

global ADANCIME_MAX
global SCMAX



class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)

def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=150,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="P1 vs CPU", valoare="1"),
            Buton(display=display, w=80, h=30, text="P1 vs P2", valoare="2"),
            Buton(display=display, w=80, h=30, text="CPU vs CPU", valoare="3")
        ],
        indiceSelectat=1)
    ok = Buton(display=display, top=250, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                        if ok.selecteazaDupacoord(pos):
                            display.fill((0, 0, 0))  # stergere ecran
                            tabla_curenta.deseneaza_grid()
                            return btn_alg.getValoare()
        pygame.display.update()




class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    GOL = '#'
    JMIN_scor = 0
    JMAX_scor = 0
    TMAX = 0
    TINCEPUT = 0
    METODA = None
    NR_LINII = None
    NR_COLOANE = None

    def __init__(self, matr=None, NR_LINII=None, NR_COLOANE=None):
        # creez proprietatea ultima_mutare # (l,c)
        self.ultima_mutare_JMAX = (int(N/2), int(M/2))
        self.ultima_mutare_JMIN = (int(N/2), int(M/2)+1)
        self.ultima_mutare = None

        if matr:
            # e data tabla, deci suntem in timpul jocului
            self.matr = matr
        else:
            # nu e data tabla deci suntem la initializare
            self.matr = [[self.__class__.GOL] * NR_COLOANE for i in range(NR_LINII)]
            if NR_LINII is not None:
                self.__class__.NR_LINII = NR_LINII
            if NR_COLOANE is not None:
                self.__class__.NR_COLOANE = NR_COLOANE

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    @classmethod
    def initializeaza(cls, display, NR_LINII=9, NR_COLOANE=10, dim_celula=80):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = [] # este lista cu patratelele din grid
        cls.NR_LINII = NR_LINII
        cls.NR_LINII = NR_COLOANE
        for linie in range(NR_LINII):
            # cls.celuleGrid.append([])
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)


    def pozitie_goala_valida(self, i, j, matr, jucator):
        # verificam cati vecini are din fiecare, returnam True daca poate sa mujte, false daca nu

        count_jucator = count_adversar = 0
        if matr[i + 1][j] == jucator:
            count_jucator += 1
        elif matr[i + 1][j] == self.jucator_opus(jucator):
            count_adversar += 1

        if i - 1 >= 0:
            if matr[i - 1][j] == jucator:
                count_jucator += 1
            elif matr[i - 1][j] == self.jucator_opus(jucator):
                count_adversar += 1

        if j + 1 < self.__class__.NR_COLOANE:
            if matr[i][j + 1] == jucator:
                count_jucator += 1
            elif matr[i][j + 1] == self.jucator_opus(jucator):
                count_adversar += 1

        if j - 1 >= 0:
            if matr[i][j - 1] == jucator:
                count_jucator += 1
            elif matr[i][j - 1] == self.jucator_opus(jucator):
                count_adversar += 1

        return count_jucator >= count_adversar

    def parcurgere(self, directie, jucator):

        if jucator == self.JMAX:
            um = self.ultima_mutare_JMAX
        else:
            um = self.ultima_mutare_JMIN
        # um = self.ultima_mutare  # (l,c)/
        print("ultima mutarea" + str(um) + " jucator " +str(jucator) )
        culoare = self.matr[um[0]][um[1]]
        nr_mutari = 0
        while True:
            um = (um[0] + directie[0], um[1] + directie[1])
            print("um vecini" + str(um))
            if not 0 <= um[0] < self.__class__.NR_LINII or not 0 <= um[1] < self.__class__.NR_COLOANE:
                break
            if not self.matr[um[0]][um[1]] == culoare:
                break
            nr_mutari += 1
        return nr_mutari

    # Piesa este aparata sau nu
    def piesaAparata(self, i, j):
        counter = 0
        ultima_mutare = None
        if self.matr[i][j] == self.JMAX:
            jucator_opus = self.JMAX
            ultima_mutare = self.ultima_mutare_JMAX
        else:
            jucator_opus = self.JMIN
            ultima_mutare = self.ultima_mutare_JMIN
        directii = [[(0, 1), (0, -1)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)], [(1, 0), (-1, 0)]]
        if i == ultima_mutare[0] and j == ultima_mutare[1]:
            return True # nu poti captura ultima mutare
        um =(i, j)
        rez = False
        for per_dir in directii:
            directii = [[i + 1, j + 1],
                        [i - 1, j - 1],
                        [i - 1, j + 1],
                        [i + 1, j - 1],
                        [i, j + 1],
                        [i, j - 1],
                        [i + 1, j],
                        [i - 1, j]]

            directii_posibile = [[linie, coloana] for [linie, coloana] in directii if
                                 0 <= linie < Joc.NR_LINII and 0 <= coloana < Joc.NR_COLOANE]


            aparare = [[linie,coloana] for [linie,coloana] in directii_posibile
                       if self.matr[linie][coloana] == jucator_opus]

            if len(aparare) >= 3:
                rez = self.matr[um[0]][um[1]]
        if rez:
            return True
        return False

    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE  # // inseamna div
            coloana = ind % self.__class__.NR_COLOANE

            if marcaj == ind:
                # daca am o patratica selectata, o desenez cu rosu
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[linie][coloana] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))

        pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)

    def final(self,jucator=None):
        t_now = time.time()
        if self.JMIN_scor >= SCMAX:
            return self.JMIN
        elif self.JMAX_scor >= SCMAX:
            return self.JMAX

        mutari = self.mutari(jucator)
        if len(mutari) != 0:
            return False
        else:
            if self.JMIN_scor> self.JMAX_scor:
                return self.JMIN_scor
            elif self.JMAX_scor > self.JMIN_scor:
                return self.JMAX_scor
            else:
                return 0
        return -1 # cazul in care nu e final


    # transforma indicele din list la coordonate la matrice
    def indice_la_pozitie(self, i):
        x = i // self.__class__.NR_COLOANE
        y = i % self.__class__.NR_COLOANE
        return x, y

    # transforma coordonatele de matrice la indice la lista
    def pozitie_la_indice(self, x, y):
        return x * self.__class__.NR_COLOANE + y


    def valid(self, i, j):
        if self.piesaAparata(i, j):
            return False
        return True



    def mutari(self, jucator):

        # print("mutareeee")
        l_mutari = []
        if jucator  == Joc.JMAX:
            um=self.ultima_mutare_JMAX
            # print("um " + str(um))
            i=um[0]
            j=um[1]
            directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]
            for direction in directions:
                if 0 <= i + direction[0] < self.__class__.NR_LINII and 0 <= j + direction[1] < self.__class__.NR_COLOANE:
                    # Eroare
                    if self.matr[i + direction[0]][j + direction[1]] == Joc.JMIN and self.valid( i + direction[0], j + direction[1]):
                        matr_tabla_noua = copy.deepcopy(self.matr)
                        # matr_tabla_noua[i][j] = "#"
                        matr_tabla_noua[i + direction[0]][j + direction[1]] = jucator
                        # Joc.JMAX_scor +=1
                        joc = Joc(matr_tabla_noua, self.__class__.NR_LINII, self.__class__.NR_COLOANE)
                        joc.ultima_mutare_JMAX = [i + direction[0], j + direction[1]]
                        l_mutari.append(joc)
                    elif  self.matr[i + direction[0]][j + direction[1]] == Joc.GOL:
                        matr_tabla_noua = copy.deepcopy(self.matr)
                        # matr_tabla_noua[i][j] = "#"
                        matr_tabla_noua[i + direction[0]][j + direction[1]] = jucator
                        joc = Joc(matr_tabla_noua, self.__class__.NR_LINII, self.__class__.NR_COLOANE)
                        joc.ultima_mutare_JMAX = [i + direction[0], j + direction[1]]
                        l_mutari.append(joc)


        elif jucator == Joc.JMIN:
            um = self.ultima_mutare_JMIN
            i = um[0]
            j = um[1]
            directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            for direction in directions:
                if 0 <= i + direction[0] < self.__class__.NR_LINII and 0 <= j + direction[1] \
                        < self.__class__.NR_COLOANE:
                    if self.matr[i + direction[0]][j + direction[1]] == Joc.JMAX and self.valid(i + direction[0],
                        j + direction[1]):
                        matr_tabla_noua = copy.deepcopy(self.matr)
                        # Joc.JMIN_scor +=1
                        # matr_tabla_noua[i][j] = "#"
                        matr_tabla_noua[i + direction[0]][j + direction[1]] = jucator
                        joc = Joc(matr_tabla_noua, self.__class__.NR_LINII, self.__class__.NR_COLOANE)
                        joc.ultima_mutare_JMIN= [i + direction[0], j + direction[1]]
                        l_mutari.append(joc)
                    elif  self.matr[i + direction[0]][j + direction[1]] == Joc.GOL:
                        matr_tabla_noua = copy.deepcopy(self.matr)
                        # matr_tabla_noua[i][j] = "#"
                        matr_tabla_noua[i + direction[0]][j + direction[1]] = jucator
                        joc = Joc(matr_tabla_noua, self.__class__.NR_LINII, self.__class__.NR_COLOANE)
                        joc.ultima_mutare_JMIN = [i + direction[0], j + direction[1]]
                        l_mutari.append(joc)
        return l_mutari

    def deseneaza_posibilitati(self, status=0, pozitii=None):
        # BONUS 15 -> se aplica pentru linie si coloana pe casuteel goale

        # cazul cand poate sa genereze un x
        if status in [0, 1]:
            if status == 0:
                culoare = (255, 255, 255)  # alb
            else:
                culoare = (102, 255, 178)  # verde
            for i in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
                linie = i // self.__class__.NR_COLOANE  # // inseamna div
                coloana = i % self.__class__.NR_COLOANE
                if self.matr[linie][coloana] == '#' and self.pozitie_goala_valida(linie, coloana, self.matr, Joc.JMIN):
                    pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[i])
        # cazul cand poate sa mute un x
        elif status == 2:
            culoare = (102, 255, 178)  # verde
            if pozitii[0] + 1 < self.__class__.NR_LINII:
                if self.matr[pozitii[0] + 1][pozitii[1]] == "#":
                    pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[
                        (pozitii[0] + 1) * self.__class__.NR_COLOANE + pozitii[1]])

            if pozitii[0] - 1 >= 0:
                if self.matr[pozitii[0] - 1][pozitii[1]] == "#":
                    pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[
                        (pozitii[0] - 1) * self.__class__.NR_COLOANE + pozitii[1]])

            if pozitii[1] + 1 < self.__class__.NR_COLOANE:
                if self.matr[pozitii[0]][pozitii[1] + 1] == "#":
                    pygame.draw.rect(self.__class__.display, culoare,
                                     self.__class__.celuleGrid[pozitii[0] * self.__class__.NR_COLOANE + pozitii[1] + 1])

            if pozitii[1] - 1 >= 0:
                if self.matr[pozitii[0]][pozitii[1] - 1] == "#":
                    pygame.draw.rect(self.__class__.display, culoare,
                                     self.__class__.celuleGrid[pozitii[0] * self.__class__.NR_COLOANE + pozitii[1] - 1])

        pygame.display.flip()

    # verifica cati vecini liberi are pozitia
    def piesa_capturabila(self, i, j, jucator):
        counter = 0
        if i + 1 < self.NR_LINIINR:
            if self.matr[i + 1, j] == Joc.jucator_opus(jucator):
                counter += 1

        if i - 1 >= 0:
            if self.matr[i - 1, j] == Joc.jucator_opus(jucator):
                counter += 1

        if j + 1 < self.NR_COLOANE:
            if self.matr[i, j + 1] == Joc.jucator_opus(jucator):
                counter += 1

        if j - 1 >= 0:
            if self.matr[i, j - 1] == Joc.jucator_opus(jucator):
                counter += 1

        return counter



    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        sir += "\n".join([str(i) + " |" + " ".join([str(x) for x in self.matr[i]]) for i in range(len(self.matr))])
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # estimeaza scorul cu doua metode
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        elif t_final == 'remiza':
            return 0
        else:  # prima estimare scor.JMAX - scor JMIN
                if Joc.METODA == 1:
                    return self.JMAX_scor - self.JMIN_scor
                else:
                    return (self.piese_capturabile(self.__class__.JMIN, 2) - self.piese_capturabile(self.__class__.JMAX, 2))


    def piese_capturabile(self, jucator, adancime):
        linii = Joc.NR_LINII
        coloane = Joc.NR_COLOANE

        p = 0
        if jucator == Joc.JMAX:
            linie = self.ultima_mutare_JMAX
            coloana = self.ultima_mutare_JMIN

        for l in range (linie- adancime, linie + adancime + 1):
            for c in range (coloana - adancime, coloana + adancime + 1):
                if l<0 or c<0 or l>=linii or c>= coloane or ( l== linie and c == coloana):
                    continue
                if self.matr[l][c] == Joc.jucator_opus(jucator) and self.piesa_capturabila(l,c, jucator) == True:
                    if(adancime != 1):
                        # Piesele mai apropiate au ponderea mai mare
                        pondere = 1
                        if(abs(linie-l)==1):
                            pondere = 4
                        if(abs(linie-l) ==2):
                            pondere = 2
                        p = (p+1)+ pondere
                    else:
                        p += 1
        return p


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None, NR_LINII = None, NR_COLOANE = None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Jucator curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """

# ok
def min_max(stare):
    if stare.tabla_joc.final() or stare.adancime == 0:
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        if stare.estimare is None:
            stare.estimare = 0
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    if stare.mutari_posibile:
        # OPTIMIZARE
        #  algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
        mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

        if mutariCuEstimare:
            if stare.j_curent == Joc.JMAX:
                # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
                stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
            else:
                # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
                stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

            stare.estimare = stare.stare_aleasa.estimare
        return stare
    else:
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        if stare.estimare is None:
            stare.estimare = 0
        return stare

# Ok
def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final(Joc.JMAX):
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)
            if not stare_noua:
                return False
            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


# Ok
def afis_daca_final(stare_curenta, jucator):
    final = stare_curenta.tabla_joc.final(jucator)
    if final == -1: # Nu e final
        return False
    if final:
        if final == 0:
            print("Remiza!")
            return True
        else:
            stare_curenta.tabla_joc.deseneaza_grid()
            print("A castigat " + str(final))
            return True





def afisare_final(): # ok
    t_dupa = int(round(time.time() * 1000))
    print("______________FINAL______________")
    # timpul total de rulare
    print("Programul a durat un timp de " + str(t_dupa - t_inainte) + " milisecunde.")
    print('----------------')
    # numarul de mutari
    print("Jucatorul a avut un numar de " + str(len(timpi_jucator)) + " mutari")
    print("Calculatorul a avut un numar de " + str(len(timpi_calculator)) + " mutari")
    print('----------------')
    # sortam timpii
    timpi_jucator.sort()
    timpi_calculator.sort()
    # cei mai mici timpi pentru fiecare jucator
    print('Cel mai mic timp de gandire al jucatorului: ' + str(timpi_jucator[0]) + " milisecunde.")
    print(
        'Cel mai mic timp de gandire al calculatorului: ' + str(timpi_calculator[0]) + " milisecunde.")
    print('----------------')
    # cei mai mari timpi pentru fiecare jucator
    print('Cel mai mare timp de gandire al jucatorului: ' + str(timpi_jucator[-1]) + " milisecunde.")
    print('Cel mai mare timp de gandire al calculatorului: ' + str(
        timpi_calculator[-1]) + " milisecunde.")
    print('----------------')
    # timpi de gandire mediani pentru fiecare jucator
    print('Timpul de gandire median al jucatorului: ' + str(
        timpi_jucator[len(timpi_jucator) // 2]) + " milisecunde.")
    print('Timpul de gandire median al calculatorului: ' + str(
        timpi_calculator[len(timpi_calculator) // 2]) + " milisecunde.")
    print('----------------')
    # timpi de gandire medii pentru fiecare jucator
    print('Timpul de gandire mediu al jucatorului: ' + str(
        sum(timpi_jucator) / len(timpi_jucator)) + " milisecunde.")
    print('Timpul de gandire mediu al calculatorului: ' + str(
        sum(timpi_calculator) / len(timpi_calculator)) + " milisecunde.")
    return



if __name__ == "__main__":

    # initializare algoritm
    t_inainte = int(round(time.time() * 1000))
    # raspuns = False
    # while not raspuns:
    #     try:
    #         SCMAX= int(input("Introduceti scorul maxim:\n "))
    #         if SCMAX:
    #             raspuns = True
    #     except:
    #         print("Va rog alegeti o varianta valida!\n")
    SCMAX = 12


    # raspuns = False
    # while not raspuns:
    #     tip_algoritm = input("Alegeti numarul corespunzator algoritmului dorit\n1.Minimax\n2.Alpha-beta\n ")
    #     if tip_algoritm in ['1', '2']:
    #         raspuns = True
    #     else:
    #         print("Va rog alegeti o varianta valida!\n.")
    tip_algoritm = 1
    # initializare tabla
    # raspuns = False
    # while not raspuns:
    #     N = int(input("Precizati N cu urmatoarele conditii: N<=10 si N>=5 si N numar impar\n"))
    #     if N>10 or N % 2 == 0 or N< 5:
    #         print( " N nu satisface condiriile dorite")
    #     else:
    #        raspuns = True
    # Joc.N = N # Numar linii
    N = 9

    # raspuns = False
    # while not raspuns:
    #     M = int(input("Precizati M cu urmatoarele conditii: M>=5 si M<=10 numar par\n"))
    #     if M<5 or M % 2 != 0 or M>10:
    #         print( " M nu satisface condiriile dorite")
    #     else:
    #        raspuns = True
    M = 10


    # raspuns = False
    # while not raspuns:
    #     Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? \n").lower()
    #     if Joc.JMIN in ['x', '0']:
    #         raspuns = True
    #     else:
    #         print("Raspunsul trebuie sa fie x sau 0.")
    # Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    Joc.JMIN='x'
    Joc.JMAX='0'
    # raspuns = False
    # while not raspuns:
    #     try:
    #         Joc.TMAX = int(input("Care este timpul maxim (secunde): \n"))
    #     except:
    #         print("Timpul introdus trebuie sa fie un numar")
    #     if Joc.TMAX > 0:
    #         raspuns = True
    #     else:
    #         print("Timpul introdus trebuie sa fie mai mare decat 0")
    Joc.TMAX=60
    raspuns = False
    metoda = 0
    # while not raspuns:
    #     try:
    #         metoda = int(
    #             input("Cum se va estima scorul?\n1.Metoda 1 - banala\n2.Metoda 2 - avansata\nAlegeti o varianta: "))
    #     except:
    #         print("Introducati o valoare din lista de mai sus")
    #     if metoda in [1, 2]:
    #         raspuns = True
    #     else:
    #         print("Introducati o valoare din lista de mai sus")
    metoda =1

    # raspuns = False
    # adancime = 0
    # while not raspuns:
    #     adancime = int(input("1.Incepator\n2.Mediu\n3.Avansat\nPrecizati nivelul de dificultate dorit: \n"))
    #     if 1 <= adancime <= 3:
    #         raspuns = True
    #     else:
    #         print("Nu ati ales o varianta corecta. Raspunsul trebuie sa fie 1, 2 sau 3")
    adancime =1

    ADANCIME_MAX = adancime
    timpi_calculator = []
    timpi_jucator = []

    # Interfata grafica
    Joc.METODA = metoda
    de_mutat=False
    pygame.init()
    pygame.display.set_caption("Alina Popescu - exemple de modificat")
    dim = 80
    linie = 1
    l1 = M *(dim + 1) - 1
    l2 = N * (dim + 1 ) - 1
    ecran = pygame.display.set_mode(size=(l1, l2))  # N *w+ N-1= N*(w+1)-1
    # ecran = pygame.display.set_mode(size=(dim_latura, dim_latura))
    Joc.initializeaza(ecran, NR_LINII=N, NR_COLOANE=M, dim_celula=dim)

    tabla_curenta=Joc(NR_LINII=N, NR_COLOANE=M)
    tabla_curenta = Joc(NR_LINII=N, NR_COLOANE=M)
    Joc.METODA = metoda
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX, NR_LINII=N, NR_COLOANE=M)
    stare_curenta.tabla_joc.matr[int(N / 2)][int(M / 2) - 1] = 'x'
    stare_curenta.tabla_joc.matr[int(N / 2)][int(M / 2)] = '0'
    print("Tabla initiala")
    print(str(tabla_curenta))
    print(len(tabla_curenta.matr))
    mod_de_joc = deseneaza_alegeri(ecran, tabla_curenta)
    tabla_curenta.deseneaza_grid()
    Joc.TINCEPUT=time.time()

while True:
    if stare_curenta.j_curent == Joc.JMIN:
        # muta jucatorul
        # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
        # l=pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                afisare_final()
                pygame.quit()  # inchide fereastra
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # click

                pos = pygame.mouse.get_pos()  # coordonatele clickului
                t_inainte = int(round(time.time() * 1000))
                for np in range(len(Joc.celuleGrid)):

                        # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                    if Joc.celuleGrid[np].collidepoint(pos):
                        # linia si coloana celulei pe care am facut click
                        linie = np // Joc.NR_COLOANE
                        coloana = np % Joc.NR_COLOANE
                        ###############################

                        if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                            if de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]:
                                # daca am facut click chiar pe patratica selectata, o deselectez
                                de_mutat = False
                                stare_curenta.tabla_joc.deseneaza_grid()
                            else:
                                de_mutat = (linie, coloana)
                                # desenez gridul cu patratelul marcat
                                stare_curenta.tabla_joc.deseneaza_grid()
                                stare_curenta.tabla_joc.deseneaza_posibilitati(2, (linie, coloana))

                        # Verificam daca e JMAX si daca putem captura
                        # ++ linii de la mine
                        elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMAX and stare_curenta.tabla_joc.valid(linie,coloana):
                            if de_mutat and (abs(linie - de_mutat[0]) > 1 or abs(coloana - de_mutat[1]) > 1):
                                print("Mutare invalida! Nu se poate muta atat de mult!\n")
                                continue
                            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                            Joc.JMIN_scor += 1
                            # plasez simbolul pe "tabla de joc"
                            # stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN

                            # afisarea starii jocului in urma mutarii utilizatorului
                            print("\nTabla dupa mutarea jucatorului")
                            print(str(stare_curenta))

                            stare_curenta.tabla_joc.deseneaza_grid()

                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                            stare_curenta.tabla_joc.ultima_mutare_JMIN = [linie, coloana]
                            # testez daca jocul a ajuns intr-o stare finala
                            # si afisez un mesaj corespunzator in caz ca da
                            if afis_daca_final(stare_curenta, Joc.JMIN):
                                break

                        elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                            if de_mutat:
                                #### eventuale teste legate de mutarea simbolului
                                if de_mutat and linie != de_mutat[0] and coloana != de_mutat[1]:
                                    print(
                                            "Mutare invalida! Mutarea trebuie sa fie pe aceeasi linie/coloana ca pozitia de unde pleaca!\n")
                                    continue
                                # trebuie pe linie, coloana sau diagonala
                                if de_mutat and (abs(linie - de_mutat[0]) > 1 or abs(coloana - de_mutat[1]) > 1):
                                    print("Mutare invalida! Nu se poate muta atat de mult!\n")
                                    continue

                                stare_curenta.tabla_joc.matr[
                                    de_mutat[0]][de_mutat[1]] = Joc.GOL
                                de_mutat = False


                            # plasez simbolul pe "tabla de joc"
                            
                            directii = [[linie+1,coloana+1],
                                            [linie-1,coloana-1],
                                            [linie-1,coloana+1],
                                            [linie+1,coloana-1],
                                            [linie,coloana+1],
                                            [linie,coloana-1],
                                            [linie+1,coloana],
                                            [linie-1,coloana]]

                            directii_posibile = [[linie,coloana] for [linie,coloana] in directii if
                                                 0 <= linie < Joc.NR_LINII and 0 <= coloana < Joc.NR_COLOANE]

                            if Joc.JMIN in [stare_curenta.tabla_joc.matr[linie_posibila][coloana_posibila]
                                            for [linie_posibila,coloana_posibila] in directii_posibile]:
                                stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                # Joc.JMIN_scor += 1
                            else:
                                break


                            # afisarea starii jocului in urma mutarii utilizatorului
                            print("\nTabla dupa mutarea jucatorului")
                            print(str(stare_curenta))
                            # print()

                            stare_curenta.tabla_joc.deseneaza_grid()
                            # testez daca jocul a ajuns intr-o stare finala
                            # si afisez un mesaj corespunzator in caz ca da
                            if afis_daca_final(stare_curenta, Joc.JMIN):
                                break

                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                            stare_curenta.tabla_joc.ultima_mutare_JMIN = [linie, coloana]

                            t_dupa = int(round(time.time() * 1000))
                            timp = t_dupa - t_inainte
                            timpi_jucator.append(timp)
                            print("Jucatorul a \"gandit\" timp de " + str(timp) + " milisecunde.")

        # --------------------------------
    else:  # jucatorul e JMAX (calculatorul)
        # Mutare calculator

        # preiau timpul in milisecunde de dinainte de mutare
        t_inainte = int(round(time.time() * 1000))
        if tip_algoritm == '1':
            stare_actualizata = min_max(stare_curenta)
        else:  # tip_algoritm==2
            stare_actualizata = alpha_beta(-500, 500, stare_curenta)

        stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
        print("Scor PC: " + str(Joc.JMAX_scor) + "   " + "Scor : " + str(Joc.JMAX_scor))
        print("Scor Utilizator: " + str(Joc.JMIN_scor) + "   " + "Scor : " + str(Joc.JMIN_scor))
        print("Tabla dupa mutarea calculatorului")
        print(str(stare_curenta))
        # print()

        stare_curenta.tabla_joc.deseneaza_grid()
        # preiau timpul in milisecunde de dupa mutare
        t_dupa = int(round(time.time() * 1000))
        timp = t_dupa - t_inainte
        timpi_calculator.append(timp)
        print("Calculatorul a \"gandit\" timp de " + str(timp) + " milisecunde.")

        if afis_daca_final(stare_curenta, Joc.JMAX):
            break

        # S-a realizat o mutare. Schimb jucatorul cu cel opus
        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            afisare_final()
            pygame.quit()
            sys.exit()







