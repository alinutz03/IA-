import math


def testare(l):
    print(len(l))
    # if len(l) % 2 !=0:
    for i in math.floor((len(l) + 1) / 2):
        for j in len(l):
            if l[i][j] != l[j][i]:
                return False

    return True



if __name__ == '__main__':
    with open('input2.txt', 'r') as f:
        l = [[int(num) for num in line.split(' ')] for line in f]
    # Prinatre linii
    print(l)


    noduri = []
    muchii =[]

    # Creare lista noduri
    for i in range(len(l)):
        noduri.append((i+1))
    i = 0

    # Creare lista muchii pentru grafuri neorientate
    for muchie in l:
        j=i
        for ind in range (i , len(muchie)):
            # print(i, j)
            if ind != 0 and i!=j:
                muchii.append([i + 1, j + 1])
            j = j+1
        i = i+1

    graf = {
        "noduri": noduri,
        "muchii": muchii
    }
    # testare(l, muchii)
    testare(l)
    print(" Graful poate fi neorinetat " + str(testare(l)))

    with open('output.txt', 'a') as f:
        f.write(str(graf))









