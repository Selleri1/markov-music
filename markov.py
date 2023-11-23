import soundfile as sf
import numpy as np


# Skapa en 7744x88-matris fylld med slumpvalda tal mellan 0 och 1
P1 = np.random.rand(7744,88)

# Gör om P1 till en övergångsmatris/stokastisk matris (summan av varje kollon ska vara 1)
# genom att dividera varje kolonn med dess summa.
# Källa: https://stackoverflow.com/questions/43644320/how-to-make-numpy-array-column-sum-up-to-1
P = P1/P1.sum(axis=0,keepdims=1)
    
# Skriv ut summan av varje kolonn för att säkerställa att de alla är 1
print(P.sum(0))
