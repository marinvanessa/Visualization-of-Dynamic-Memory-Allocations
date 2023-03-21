# Clasa reprezinta un call de malloc

class malloc_call:
    def __init__(self, dimension, allocation_time)-> None:
        # dimensiunea memoriei alocate
        self.dimension = dimension 
        # timpul de la care incepe alocarea
        self.allocation_time = allocation_time
        # timpul la care se sfarseste alocarea
        self.end_allocation_time = -1
        # adresa intiala
        self.addr = -1
