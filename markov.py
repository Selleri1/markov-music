import numpy as np
import random

# Intervallet av toner i midi-standarden vi ska använda (det finns 0 till (och inte med) 128)
# Detta bestämmer storleken på matrisen.
LOWER_LIMIT = 60#0
# UPPER_LIMIT inkluderas inte
UPPER_LIMIT = 62#128

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

def markov(x: np.ndarray, P: np.ndarray) -> np.ndarray:
    """Utför formeln för markovkedjan. Tar in ett x_k och returnerar ett x_(k+1) med
    matrisen P."""
    return P @ x

    
def make_prob_matrix(song_as_list: list[int]) -> np.ndarray:
    """Tar en lista som är alla toner i en sång (en sådan genererad av read_midi.read_midi) och returnerar
    en matris med sannolikheterna att en viss ton leder till en annan. Matrisen har storleken"""
    num_notes = UPPER_LIMIT-LOWER_LIMIT
    matrix = np.empty(shape=(num_notes, num_notes))
    # Loopa igenom alla möjliga toner
    for note in range(LOWER_LIMIT, UPPER_LIMIT):
        song = song_as_list.copy()
        # Listan här räknar hur många gånger varje ton förekommer efter 'note'
        # Om tonen 50 kom efter 'note' 5 gånger så blir note_occurances[50] == 5
        # Om LOWER_LIMIT är 5 så kommer note_occurances[0] att motsvara ton 5
        note_occurances = [0 for _ in range(num_notes)]
        while True:
            try:
                # Hitta nästa gång 'note' framkommer i listan
                note_index = song.index(note)
            except ValueError:
                # Om song.index skickar ValueError så fanns inte tonen i listan. Avsluta while-loopen
                break
            
            if note_index == len(song) - 1:
                # Om det var sista tonen i sången
                break
            
            song.pop(note_index)
            # Nu är den tonen som kom efter på index 'note_index'
            note_occurances[song[note_index] - LOWER_LIMIT] += 1
            
        if sum(note_occurances) == 0:
            # Om 'note' aldrig fanns i sången kommer listan vara tom.
            # Gör i så fall en sannolikhetsmatris med samma sannolikhet för allt.
            # Osäker på hur vi ska göra här.
            prob_vector = np.ones(num_notes)
        else:
            prob_vector = np.array(note_occurances)
            
        # Se till att summan är 1
        prob_vector = make_col_sum_one(prob_vector)
        # Sätt kollonnen för den här tonen till den normaliserade sannolikhetsvektorn
        matrix[:,note - LOWER_LIMIT] = prob_vector
    return matrix
        
    
def make_col_sum_one(array: np.ndarray) -> np.ndarray:
    # Dividera varje kolonn med dess summa.
    # Källa: https://stackoverflow.com/questions/43644320/how-to-make-numpy-array-column-sum-up-to-1
    return array/array.sum(axis=0,keepdims=1)
        

def main():
    # Storleken på matrisen. Vektorerna kommer ha storleken COL. 
    COL = 88
    ROW = 88

    # Skapa en COL x ROW-matris fylld med slumpvalda tal mellan 0 och 1.
    P1 = np.random.rand(COL, ROW)

    P = make_col_sum_one(P1)
        
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
        
    print(make_prob_matrix([60, 61, 61, 60, 61]))
    
if __name__ == "__main__":
    main()

# (7744x88) andra ordningen?