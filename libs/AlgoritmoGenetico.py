import json
import random
import matplotlib.pyplot as plt
import os


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
        self.id_readed = []
        for book in input_data["history"]:
            self.id_readed.append(book["id"])
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

    def poda(self, population):
        while (len(population) > self.max_population):
            index_to_delete = random.randrange(0, len(population))
            del population[index_to_delete]
        return population

    def calculate_from_population(self, gen_list):
        logs = []
        best = None
        worst = None
        total_weight = 0
        ids_checked = []

        for individual in gen_list:
            individual_as_index = int(str(individual), 2)
            individual_weight = 0

            if (individual_as_index >= len(self.data)):
                # Se puede comentar esta línea si se quiere omitir los individuos fuera de rango. (Para evitar que la gráfica del peor individuo llegue a 0 tan rápido)
                logs.append({"gen": individual,
                            "weight": individual_weight})
                # print("Skipping due to index being larger than the dataset...")
                continue

            current_individual_authors = self.data[individual_as_index]["autores"]
            current_individual_categories = self.data[individual_as_index]["categorias"]
            current_individual_id = self.data[individual_as_index]["autores"]
            
            if (current_individual_id in ids_checked):
                # El libro que checamos ya está calculado, podemos omitirlo para evitar libros duplicados en el resultado
                continue
            
            if(current_individual_id in self.id_readed):
                # El libro que estamos calculando ya es un libro que el usuario ha leido, omitimos para no recomenndar un libro del usuario.
                continue
            
            ids_checked.append(current_individual_id)
            
            if any(item in self.readed_authors for item in current_individual_authors):
                individual_weight += 1
            if any(item in self.favorites_authors for item in current_individual_authors):
                individual_weight += 1
            if any(item in self.readed_categories for item in current_individual_categories):
                individual_weight += 1
            if any(item in self.favorites_categories for item in current_individual_categories):
                individual_weight += 1

            individual_to_save = {"gen": individual,
                                  "weight": individual_weight}
            logs.append(individual_to_save)
            total_weight += individual_weight

            if (best is None and worst is None):
                best = individual_to_save
                worst = individual_to_save
                continue

            if (best["weight"] < individual_weight):
                best = individual_to_save

            if (worst["weight"] > individual_weight):
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

    def search_from_index(self, books_list):
        result = []

        for book_index_bin in books_list:
            individual_as_index = int(str(book_index_bin["gen"]), 2)

            if (individual_as_index >= len(self.data)):
                print(f"Saltando libro {book_index_bin}, fuera de rango.")
                continue

            res = self.data[individual_as_index]
            res["weight"] = book_index_bin["weight"]
            result.append(res)

        return result

    def render_graphics(self):

        average_values = [entry['avarage'] for entry in self.all_records]
        best_weights = [entry['best']['weight'] for entry in self.all_records]
        worst_weights = [entry['worst']['weight']
                         for entry in self.all_records]

        indices = list(range(len(self.all_records)))

        plt.figure(figsize=(12, 6))
        # Crear la gráfica
        plt.plot(indices, average_values, marker='o', linestyle='-',
                 label='Pesos promedios', color='blue')
        plt.plot(indices, best_weights, marker='o',
                 linestyle='-', label='Mejor Peso', color='green')
        plt.plot(indices, worst_weights, marker='o',
                 linestyle='-', label='Peor Peso', color='red')

        # Añadir etiquetas y título
        plt.xlabel('Generación')
        plt.ylabel('Peso')
        plt.title('Reporte Histórico')
        plt.legend()

        # Mostrar la gráfica
        plt.grid(True)
        carpeta = "graphics"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Guardar la gráfica en la carpeta
        ruta_grafica = os.path.join(carpeta, "grafica.png")
        plt.savefig(ruta_grafica)

    def run(self, max_result=10):
        # Inicialización
        result = None
        best_individual = {"gen": None, "weight": None}
        worst_individual = {"gen": None, "weight": None}

        self.all_records = []
        # Invoca la primera generación
        population = self.invoke_first_generation()

        # --genarational loop--
        for i in range(self.generations_count):
            print(f"Generación {i+1} de {self.generations_count}")
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
            # Guardamos las estadísticas en memoria para posterior
            # Todo el registro para la gráfica posterior

            if (best_individual["gen"] is not None):
                best_individual = best_individual if best_individual["weight"] > result[
                    "stats"]["best"]["weight"] else result["stats"]["best"]
            else:
                best_individual = result["stats"]["best"]

            if (worst_individual["gen"] is not None):
                worst_individual = worst_individual if worst_individual["weight"] < result[
                    "stats"]["worst"]["weight"] else result["stats"]["worst"]
            else:
                worst_individual = result["stats"]["worst"]

            result["stats"]["best"] = best_individual
            self.all_records.append(result["stats"])

            if (len(population) > self.max_population):
                population = self.poda(population)

        return self.search_from_index(sorted(result['logs'], key=lambda x: x['weight'], reverse=True)[:max_result])
