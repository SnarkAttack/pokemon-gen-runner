from pyboy import PyBoy

class PokemonPyBoyWrapper(PyBoy):

    def __init__(self, gamerom_file, **kwargs):
        print("Start")
        super().__init__(gamerom_file, **kwargs)

    

