import soundfile as sf
import numpy as np

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
    for i in range(10000):
        x = markov(x, P)
        if i >= 10000-5:
            print(x[85:], end="\n--------\n") 
    
    # Jag försökte lösa vad kedjan ska konvergera mot men
    # det är svårt att lösa ekvationssystem med mer än en lösning med numpy...
    #q = np.linalg.solve(P - np.eye(ROW, COL), np.zeros((COL, 1)))
    #print(q[85:])
    
if __name__ == "__main__":
    main()

# (7744x88) andra ordningen?
