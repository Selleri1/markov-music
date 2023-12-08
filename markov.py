import soundfile as sf
import numpy as np
import random

def generate_random_boolean(probability_true):
    return random.random() < probability_true

def binary_vector(prob_vector):
    bi_vector=[]
    for y in range(len(prob_vector)):
        bi_vector.append(prob_vector[y][0])
    print(bi_vector[0])
    summa=1
    for x in range(len(bi_vector)):
        if x!=len(bi_vector)-1:
            if generate_random_boolean(bi_vector[x]/summa):
                bi_vector[x]=1
                bi_vector[x+1:] = [0] * (len(bi_vector)-x-1)
                break
            else:
                bi_vector[x]=0
                summa-=bi_vector[x]
        else:
            bi_vector[x]=1
    print(bi_vector)
    return bi_vector

def markov(x: np.ndarray, P: np.ndarray):
    """Utför formeln för markovkedjan. Tar in ett x_k och returnerar ett x_(k+1) med
    matrisen P."""
    return P @ x

def main():
    # Storleken på matrisen. Vektorerna kommer ha storleken COL. 
    COL = 88
    ROW = 88

    # Skapa en COL x ROW-matris fylld med slumpvalda tal mellan 0 och 1.
    P1 = np.random.rand(COL, ROW)

    # Gör om P1 till en övergångsmatris/stokastisk matris (summan av varje kollon ska vara 1)
    # genom att dividera varje kolonn med dess summa.
    # Källa: https://stackoverflow.com/questions/43644320/how-to-make-numpy-array-column-sum-up-to-1
    P = P1/P1.sum(axis=0,keepdims=1)
        
    # Skriv ut summan av varje kolonn för att säkerställa att de alla är 1
    print(P.sum(0))

    # Sannolikhetsvektorn (state vector) som kedjan startar med
    x0 = np.zeros((COL, 1))
    x0[3] = 1
    
    print(x0)
    
    #Testa 10000 iterationer av markov för att se att x konvergerar mot något
    x = x0
    lista_av_sannolikhetsvektorer=[]
    for i in range(10000):
        x = markov(x, P)
        lista_av_sannolikhetsvektorer.append(x)
        if i >= 10000-5:
            print(x[85:], end="\n--------\n") 
    
    # Jag försökte lösa vad kedjan ska konvergera mot men
    # det är svårt att lösa ekvationssystem med mer än en lösning med numpy...
    #q = np.linalg.solve(P - np.eye(ROW, COL), np.zeros((COL, 1)))
    #print(q[85:])
    lista_av_toner=[]
    for x in range(len(lista_av_sannolikhetsvektorer)):
        lista_av_toner.append(binary_vector(lista_av_sannolikhetsvektorer[x]))
    
if __name__ == "__main__":
    main()

# (7744x88) andra ordningen?