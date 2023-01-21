import time

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
        N = int(input("Precizati N cu urmatoarele conditii: N>=10 si N numar impar"))
        if N<10 or N % 2 == 0:
            print( " N nu satisface condiriile dorite")
        else:
           raspuns = True

    raspuns = False
    while not raspuns:
        M = int(input("Precizati N cu urmatoarele conditii: M>=5 si M numar par"))
        if M<5 or N % 2 != 0:
            print( " M nu satisface condiriile dorite")
        else:
           raspuns = True

    # initializare jucatori
    # raspuns = False
    # while not raspuns:
    #     Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
    #     if Joc.JMIN in ['x', '0']:
    #         raspuns = True
    #     else:
    #         print("Raspunsul trebuie sa fie x sau 0.")
    # Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    #
    # raspuns = False
    # while not raspuns:
    #     try:
    #         Joc.TMAX = int(input("Care este timpul maxim (secunde): "))
    #     except:
    #         print("Timpul introdus trebuie sa fie un numar")
    #     if Joc.TMAX > 0:
    #         raspuns = True
    #     else:
    #         print("Timpul introdus trebuie sa fie mai mare decat 0")

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
