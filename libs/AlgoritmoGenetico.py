import json


class AlgoritmoGenetico:
    def __init__(self):
        print("Importando dataset...")
        with open("dataset/cleareddata.json", "r",  encoding="utf8") as f:
            self.datos = json.load(f)

        self.bit_size = self.calculate_bit_size(len(self.datos))
        pass

    # Calcula el tamaño de dígito que tendrá el gen, si es 4 => "0101".
    def calculate_bit_size(self, numero):
        return len(bin(numero))-2

    def setup(self, porcentaje_cruza=0.5, porcentaje_mut_ind=0.5, porcentaje_mut_gen=0.5, poblacion_inicial=10, poblacion_max=40, generaciones=100):
        self.cross_prob = porcentaje_cruza
        self.individual_mut_prob = porcentaje_mut_ind
        self.gen_mut_prob = porcentaje_mut_gen
        self.initial_population = poblacion_inicial
        self.max_population = poblacion_max
        self.generations_count = generaciones
        pass
