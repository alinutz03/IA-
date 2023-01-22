import math
import sys
import time
import pygame


def elem_identice(lista):
	if(len(set(lista))==1) :
		return lista[0] if lista[0]!=Joc.GOL else False
	return False

global ADANCIME_MAX


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


    @classmethod
    def initializeaza(cls, display, NR_COLOANE=None,NR_LINII=None, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_LINII):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def __init__(self, matr=None, NR_LINII=None, NR_COLOANE=None):
        self.ultima_mutare = None
        if matr:
            # e data tabla, deci suntem in timpul jocului
            self.matr = matr
        else:
            # nu e data tabla deci suntem la initializare
            self.matr = matr or [self.__class__.GOL] * NR_COLOANE * NR_LINII

            if NR_LINII is not None:
                self.__class__.NR_LINII = NR_LINII
            if NR_COLOANE is not None:
                self.__class__.NR_COLOANE = NR_COLOANE

    # DE LIPIT X SI O

    # def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]
    #
    #     for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
    #         linie = ind // self.__class__.NR_COLOANE  # // inseamna div
    #         coloana = ind % self.__class__.NR_COLOANE
    #
    #         if marcaj == ind:
    #             # daca am o patratica selectata, o desenez cu rosu
    #             culoare = (255, 0, 0)
    #         else:
    #             # altfel o desenez cu alb
    #             culoare = (255, 255, 255)
    #         pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
    #         if self.matr[linie][coloana] == 'x':
    #             self.__class__.display.blit(self.__class__.x_img, (
    #                 coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
    #         elif self.matr[linie][coloana] == '0':
    #             self.__class__.display.blit(self.__class__.zero_img, (
    #                 coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
    #
    #     pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)
    def pozitie_goala_valida(self, i, j, matr, jucator):
        return
    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(len(self.matr)):
            linie = ind // self.__class__.NR_COLOANE  # // inseamna div
            coloana = ind % self.__class__.NR_COLOANE

            if marcaj == ind:
                 # daca am o patratica selectata, o desenez cu rosu
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                   self.__class__.display.blit(self.__class__.zero_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)



    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        t_now = time.time()
        if t_now - self.TINCEPUT > self.TMAX:
            if self.JMIN_scor == self.JMAX_scor:
                return 'remiza'
            return self.JMIN if self.JMIN_scor > self.JMAX_scor else self.JMAX
        return False

    # transforma indicele din list la coordonate la matrice
    def indice_la_pozitie(self, i):
        x = i // self.dimensiune_tabla
        y = i % self.dimensiune_tabla
        return x, y

    # transforma coordonatele de matrice la indice la lista
    def pozitie_la_indice(self, x, y):
        return x * self.dimensiune_tabla + y

    def mutari(self, jucator):
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == self.__class__.GOL:
                # se genereza simboluri doar pe laterale
                if (jucator == '0' and (0 < i < self.dimensiune_tabla or not (i + 1) % self.dimensiune_tabla)) \
                        or (jucator == 'x' and (self.dimensiune_tabla ** 2 - (
                        self.dimensiune_tabla - 1) < i < self.dimensiune_tabla or not i % self.dimensiune_tabla)):
                    matr_tabla_noua = list(self.matr)
                    matr_tabla_noua[i] = jucator
                    # functie verif configuratie refaci tabla
                    l_mutari.append(Joc(matr_tabla_noua, self.dimensiune_tabla))
            elif self.matr[i] == self.__class__.JMAX:
                N = S = E = V = True
                # se muta elemente cu max ceil(N/3) + 1
                for numar_patrate_mutate in range(1, math.ceil(self.dimensiune_tabla / 3) + 1):
                    x, y = self.indice_la_pozitie(i)
                    # S - verificare pozitii
                    if self.pozitie_la_indice(x + numar_patrate_mutate, y) < self.dimensiune_tabla and S:
                        if self.matr[self.pozitie_la_indice(x + numar_patrate_mutate, y)] == "#":
                            matr_tabla_noua = list(self.matr)
                            matr_tabla_noua[i] = "#"
                            matr_tabla_noua[self.pozitie_la_indice(x + numar_patrate_mutate, y)] = jucator
                            l_mutari.append(Joc(matr_tabla_noua, self.dimensiune_tabla))
                        else:
                            S = False

                    # N - verificare pozitii
                    if self.pozitie_la_indice(x - numar_patrate_mutate, y) >= 0 and N:
                        if self.matr[self.pozitie_la_indice(x - numar_patrate_mutate, y)] == "#":
                            matr_tabla_noua = list(self.matr)
                            matr_tabla_noua[i] = "#"
                            matr_tabla_noua[self.pozitie_la_indice(x - numar_patrate_mutate, y)] = jucator
                            l_mutari.append(Joc(matr_tabla_noua, self.dimensiune_tabla))
                        else:
                            N = False

                    # V - verificare pozitii
                    if self.pozitie_la_indice(x, y - numar_patrate_mutate) >= 0 and V:
                        if self.matr[self.pozitie_la_indice(x, y - numar_patrate_mutate)] == "#":
                            matr_tabla_noua = list(self.matr)
                            matr_tabla_noua[i] = "#"
                            matr_tabla_noua[self.pozitie_la_indice(x, y - numar_patrate_mutate)] = jucator
                            l_mutari.append(Joc(matr_tabla_noua, self.dimensiune_tabla))
                        else:
                            V = False
                    # E - verificare pozitii
                    if self.pozitie_la_indice(x, y + numar_patrate_mutate) < self.dimensiune_tabla and E:
                        if self.matr[self.pozitie_la_indice(x, y + numar_patrate_mutate)] == "#":
                            matr_tabla_noua = list(self.matr)
                            matr_tabla_noua[i] = "#"
                            matr_tabla_noua[self.pozitie_la_indice(x, y + numar_patrate_mutate)] = jucator
                            l_mutari.append(Joc(matr_tabla_noua, self.dimensiune_tabla))
                        else:
                            E = False

        return l_mutari

    # verifica cati vecini liberi are pozitia
    def verif_directii(self, i, j, jucator):
        counter = 0
        if i + 1 < self.dimensiune_tabla:
            if self.matr[self.pozitie_la_indice(i + 1, j)] == "#":
                counter += 1

        if i - 1 >= 0:
            if self.matr[self.pozitie_la_indice(i - 1, j)] == "#":
                counter += 1

        if j + 1 < self.dimensiune_tabla:
            if self.matr[self.pozitie_la_indice(i, j + 1)] == "#":
                counter += 1

        if j - 1 >= 0:
            if self.matr[self.pozitie_la_indice(i, j - 1)] == "#":
                counter += 1

        return counter

    # piede capturabile - genereaza un scor bazat pe nr de vecini liberii ai adversarului * pondere
    def numar_piese_capturabile(self, jucator):
        # pondere pentru numarul de vecini liberi
        scores = [0, 2, 4, 6, 8]
        total = 0
        for i in range(self.dimensiune_tabla):
            for j in range(self.dimensiune_tabla):
                if self.matr[self.pozitie_la_indice(i, j)] == self.jucator_opus(jucator):
                    vecini = self.verif_directii(i, j, jucator)
                    total += vecini * scores[vecini]

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
                return self.numar_piese_capturabile(self.JMAX) - self.numar_piese_capturabile(self.JMIN)

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_LINII):  # itereaza prin linii
            sir += str(i) + " |" + " ".join(
                [str(x) for x in self.matr[self.NR_COLOANE * i: self.NR_COLOANE * (i + 1)]]) + "\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


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


def min_max(stare):
    if stare.tabla_joc.final() or stare.adancime == 0:
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        if stare.estimare is None:
            stare.estimare = 0
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    if stare.mutari_posibile:
        # BONUS 12
        # stare.mutari_posibile.sort(key=lambda x: x.estimare)
        # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
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


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
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


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def verificare_configuratie(tabla_curenta, stare_curenta, linie, coloana):
    return


def afisare_final():
    # t_dupa = int(round(time.time() * 1000))
    # print("______________FINAL______________")
    # # timpul total de rulare
    # print("Programul a durat un timp de " + str(t_dupa - t_inainte) + " milisecunde.")
    # print('----------------')
    # # numarul de mutari
    # print("Jucatorul a avut un numar de " + str(len(timpi_jucator)) + " mutari")
    # print("Calculatorul a avut un numar de " + str(len(timpi_calculator)) + " mutari")
    # print('----------------')
    # # sortam timpii
    # timpi_jucator.sort()
    # timpi_calculator.sort()
    # # cei mai mici timpi pentru fiecare jucator
    # print('Cel mai mic timp de gandire al jucatorului: ' + str(timpi_jucator[0]) + " milisecunde.")
    # print(
    #     'Cel mai mic timp de gandire al calculatorului: ' + str(timpi_calculator[0]) + " milisecunde.")
    # print('----------------')
    # # cei mai mari timpi pentru fiecare jucator
    # print('Cel mai mare timp de gandire al jucatorului: ' + str(timpi_jucator[-1]) + " milisecunde.")
    # print('Cel mai mare timp de gandire al calculatorului: ' + str(
    #     timpi_calculator[-1]) + " milisecunde.")
    # print('----------------')
    # # timpi de gandire mediani pentru fiecare jucator
    # print('Timpul de gandire median al jucatorului: ' + str(
    #     timpi_jucator[len(timpi_jucator) // 2]) + " milisecunde.")
    # print('Timpul de gandire median al calculatorului: ' + str(
    #     timpi_calculator[len(timpi_calculator) // 2]) + " milisecunde.")
    # print('----------------')
    # # timpi de gandire medii pentru fiecare jucator
    # print('Timpul de gandire mediu al jucatorului: ' + str(
    #     sum(timpi_jucator) / len(timpi_jucator)) + " milisecunde.")
    # print('Timpul de gandire mediu al calculatorului: ' + str(
    #     sum(timpi_calculator) / len(timpi_calculator)) + " milisecunde.")
    return



if __name__ == "__main__":

    # initializare algoritm
    t_inainte = int(round(time.time() * 1000))
    raspuns = False
    while not raspuns:
        tip_algoritm = input("Alegeti numarul corespunzator algoritmului dorit\n1.Minimax\n2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns = True
        else:
            print("Va rog alegeti o varianta valida!\n.")

    # initializare tabla
    raspuns = False
    while not raspuns:
        N = int(input("Precizati N cu urmatoarele conditii: N>=10 si N numar impar\n"))
        if N<9 or N % 2 == 0:
            print( " N nu satisface condiriile dorite")
        else:
           raspuns = True
    # Joc.N = N # Numar linii

    raspuns = False
    while not raspuns:
        M = int(input("Precizati M cu urmatoarele conditii: M>=5 si M numar par\n"))
        if M<5 or M % 2 != 0:
            print( " M nu satisface condiriile dorite")
        else:
           raspuns = True


    raspuns = False
    while not raspuns:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? \n").lower()
        if Joc.JMIN in ['x', '0']:
            raspuns = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    #
    raspuns = False
    while not raspuns:
        try:
            Joc.TMAX = int(input("Care este timpul maxim (secunde): \n"))
        except:
            print("Timpul introdus trebuie sa fie un numar")
        if Joc.TMAX > 0:
            raspuns = True
        else:
            print("Timpul introdus trebuie sa fie mai mare decat 0")

    raspuns = False
    metoda = 0
    while not raspuns:
        try:
            metoda = int(
                input("Cum se va estima scorul?\n1.Metoda 1 - banala\n2.Metoda 2 - avansata\nAlegeti o varianta: "))
        except:
            print("Introducati o valoare din lista de mai sus")
        if metoda in [1, 2]:
            raspuns = True
        else:
            print("Introducati o valoare din lista de mai sus")

    raspuns = False
    adancime = 0
    while not raspuns:
        adancime = int(input("1.Incepator\n2.Mediu\n3.Avansat\nPrecizati nivelul de dificultate dorit: \n"))
        if 1 <= adancime <= 3:
            raspuns = True
        else:
            print("Nu ati ales o varianta corecta. Raspunsul trebuie sa fie 1, 2 sau 3")

    ADANCIME_MAX = adancime
    timpi_calculator = []
    timpi_jucator = []


    tabla_curenta = Joc(NR_LINII = N, NR_COLOANE = M)
    Joc.METODA=metoda
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX, NR_LINII = N, NR_COLOANE = M)
    p1 = int(N/2)
    stare_curenta.tabla_joc.matr[int((p1 * M) + M/2)-1] = 'x'
    stare_curenta.tabla_joc.matr[int((p1 * M) + M/2 )] = '0'

    print("Tabla initiala")
    print(str(tabla_curenta))

    # Interfata grafica
    Joc.METODA = metoda
    de_mutat=False
    pygame.init()
    pygame.display.set_caption("Alina Popescu - exemple de modificat")
    dim = 70
    ecran = pygame.display.set_mode(size=(M * (dim + 1) - 1, N * (dim + 1) - 1))
    Joc.initializeaza(ecran, NR_LINII=N, NR_COLOANE=M, dim_celula=dim)
    tabla_curenta.deseneaza_grid()
    Joc.TINCEPUT=time.time()


    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # Muta jucatorul
            # if not de_mutat:
            #     stare_curenta.tabla_joc.deseneaza_posibilitati(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    afisare_final()
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    t_inainte = int(round(time.time() * 1000))
                    for np in range(len(Joc.celuleGrid)):
                        if Joc.celuleGrid[np].collidepoint(pos):
                            linie = np // Joc.NR_COLOANE
                            coloana = np % Joc.NR_COLOANE

                            if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                                if de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]:
                                    # daca am facut click chiar pe patratica selectata, o deselectez
                                    de_mutat = False
                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    # stare_curenta.tabla_joc.deseneaza_posibilitati(0)

                                else:
                                    de_mutat = (linie, coloana)
                                    # desenez gridul cu patratelul marcat
                                    stare_curenta.tabla_joc.deseneaza_grid(np)
                                    # desenez posinilitatile apropriate
                                    stare_curenta.tabla_joc.deseneaza_posibilitati(2, (linie, coloana))

                            elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                if de_mutat:
                                    #### eventuale teste legate de mutarea simbolului
                                    if de_mutat and (abs(linie - de_mutat[0]) > 1 or abs(coloana - de_mutat[1]) > 1):
                                        print("Mutare invalida! Nu se poate muta atat de mult!\n")
                                        continue
                                    stare_curenta.tabla_joc.matr[de_mutat[0]][de_mutat[1]] = Joc.GOL
                                    de_mutat = False

                                elif not Joc.pozitie_goala_valida(tabla_curenta, linie, coloana,
                                                                      stare_curenta.tabla_joc.matr,
                                                                      stare_curenta.j_curent):
                                    print("Mutare invalida! Nu se poate muta langa mai multi adversari!\n")
                                    continue

                                    stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN

                                    # afisarea starii jocului in urma mutarii utilizatorului
                                    print("\nTabla dupa mutarea jucatorului")
                                    print(str(stare_curenta))

                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    # testez daca jocul a ajuns intr-o stare finala
                                    # si afisez un mesaj corespunzator in caz ca da
                                    if afis_daca_final(stare_curenta):
                                        break

                                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                    # preiau timpul in milisecunde de dupa mutare
                                t_dupa = int(round(time.time() * 1000))
                                timp = t_dupa - t_inainte
                                timpi_jucator.append(timp)
                                print("Jucatorul a \"gandit\" timp de " + str(timp) + " milisecunde.")
                                stare_curenta.tabla_joc.ultima_mutare = [linie, coloana]
                                # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
                print("Estimare min-max: " + str(stare_actualizata.scor))
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                print("Estimare alpha-beta: " + str(stare_actualizata.scor))
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

        # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timp = t_dupa - t_inainte
            timpi_calculator.append(timp)
            print("Calculatorul a \"gandit\" timp de " + str(timp) + " milisecunde.")

            stare_curenta.tabla_joc.deseneaza_grid()
            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                afisare_final()
                pygame.quit()
                sys.exit()






