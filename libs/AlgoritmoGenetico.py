import json
import random
from pprint import pp


class AlgoritmoGenetico:
    def __init__(self):
        print("Importando dataset...")

        # TODO: Modificar si no se usará el json como alimentación del algoritmo
        with open("dataset/cleareddata.json", "r",  encoding="utf8") as f:
            self.data = json.load(f)

        self.bit_size = self.calculate_bit_size(len(self.data))
        pass

    # Calcula el tamaño de dígito que tendrá el gen, si es 4 => "0101".
    def calculate_bit_size(self, numero):
        return len(bin(numero))-2

    def setup(self, porcentaje_cruza=0.5, porcentaje_mut_ind=0.5, porcentaje_mut_gen=0.5, poblacion_inicial=10, poblacion_max=40, generaciones=100):
        """Inicializa los valores adicionales del algoritmo genético

        Args:
            porcentaje_cruza (float, optional): _description_. Defaults to 0.5.
            porcentaje_mut_ind (float, optional): _description_. Defaults to 0.5.
            porcentaje_mut_gen (float, optional): _description_. Defaults to 0.5.
            poblacion_inicial (int, optional): _description_. Defaults to 10.
            poblacion_max (int, optional): _description_. Defaults to 40.
            generaciones (int, optional): _description_. Defaults to 100.
        """
        self.cross_prob = porcentaje_cruza
        self.individual_mut_prob = porcentaje_mut_ind
        self.gen_mut_prob = porcentaje_mut_gen
        self.initial_population = poblacion_inicial
        self.max_population = poblacion_max
        self.generations_count = generaciones
        pass

    def load_preferences(self, input_data):
        """Vierte los datos de entrada en arrays para su mejor manejo y validaciones

        Args:
            input_data (dict): Diccionario con los datos de entrada
        """
        self.favorites_categories = input_data["favorites"]["categories"]
        self.favorites_authors = input_data["favorites"]["authors"]
        self.readed_categories = []
        self.readed_authors = []
        for book in input_data["history"]:
            self.readed_authors.extend(book["autores"])
            self.readed_categories.extend(book["categorias"])

    def random_individual_gen(self):
        result = ""

        for _ in range(self.bit_size):
            result = result + str(random.randrange(0, 2, 1))

        return result

    def invoke_first_generation(self):
        result = []

        for _ in range(self.initial_population):
            result.append(self.random_individual_gen())
        return result

    def calculate_from_population(self, gen_list):
        logs = []
        best = None
        worst = None
        total_weight = 0

        for individual in gen_list:
            individual_as_index = int(str(individual), 2)
            individual_weight = 0

            if (individual_as_index >= len(self.data)):
                # Se puede comentar esta línea si se quiere omitir los individuos fuera de rango. (Para evitar que la gráfica del peor individuo llegue a 0 tan rápido)
                logs.append({"individual": individual,
                            "weight": individual_weight})
                print("Skipping due to index being larger than the dataset...")
                continue

            current_individual_authors = self.data[individual_as_index]["autores"]
            current_individual_categories = self.data[individual_as_index]["categorias"]

            if any(item in self.readed_authors for item in current_individual_authors):
                individual_weight += 1
            if any(item in self.favorites_authors for item in current_individual_authors):
                individual_weight += 1
            if any(item in self.readed_categories for item in current_individual_categories):
                individual_weight += 1
            if any(item in self.favorites_categories for item in current_individual_categories):
                individual_weight += 1

            individual_to_save = {"individual": individual, "weight": individual_weight}
            logs.append(individual_to_save)
            total_weight += individual_weight
            
            if(best is None and worst is None):
                best = individual_to_save
                worst = individual_to_save
                continue

            if(best["weight"] < individual_weight):
                best = individual_to_save
                
            if(worst["weight"] > individual_weight):
                worst = individual_to_save

        return {"logs": logs, "stats": {"best": best, "worst": worst, "avarage": round(total_weight / len(gen_list), 3)}}

    def cross(self, population):
        result = []
        for individual in population:
            if random.uniform(0.01, 1.00) <= self.cross_prob:
                individual_to_cross = population[random.randrange(
                    0, len(population)-1)]
                result.append(self.exchange_gen(
                    individual, individual_to_cross))

            if random.uniform(0.01, 1.00) <= self.individual_mut_prob:
                individual = self.mutate_individual(individual)
            result.append(individual)

        return result

    def mutate_individual(self, individual):
        mutated_individual = list(individual)

        for bit in range(len(individual)):
            if random.uniform(0.01, 1.00) <= self.gen_mut_prob:
                index = random.randrange(0, len(mutated_individual))
                mutated_individual[bit] = individual[index]
                mutated_individual[index] = individual[bit]

        return "".join(mutated_individual)

    def exchange_gen(self, original_individual, individual_to_cross):
        genetic_chain = list(original_individual)
        another_genetic_chain = individual_to_cross

        bits_for_exchanges = random.sample(
            range(len(genetic_chain)), random.randrange(1, len(genetic_chain) + 1))

        for bit in bits_for_exchanges:
            genetic_chain[bit] = another_genetic_chain[bit]

        return "".join(genetic_chain)

    def run(self):
        # Inicialización
        best_individual = {"gen": None, "weight": None}
        worst_individual = {"gen": None, "weight": None}

        all_records = []
        # Invoca la primera generación
        population = self.invoke_first_generation()

        # --genarational loop--
        # Cruzamos la primera generación
        population = self.cross(population)

        if (best_individual["gen"] is not None):
            if (best_individual["gen"] not in population):
                # Metemos a la fuerza al mejor individuo si se perdió o mutó durante el crossing
                population[random.randrange(
                    0, len(population))] = best_individual["gen"]

        if (worst_individual["gen"] is not None):
            if (worst_individual["gen"] not in population):
                # Metemos a la fuerza al peor individuo si se perdió o mutó durante el crossing
                population[random.randrange(
                    0, len(population))] = worst_individual["gen"]

        result = self.calculate_from_population(population)
        pp(result)
