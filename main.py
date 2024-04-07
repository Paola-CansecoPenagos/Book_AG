from libs.AlgoritmoGenetico import AlgoritmoGenetico
import json

"""
Importamos los datos de entrada
Los datos de entrada son de esta forma: (ver dataset(sample_input.json))
{
    favorites:{
        categories: [<Array de string de categorias existentes sde dataset/categories.json>],
        authors: [<Array de string de autores existentes sde dataset/authors.json>]
    },
    history:[<Array de libros como aparecen en dataset/cleareddata.json>]
}

Puedes usar "node tools/generate_random_input_data.mjs 12 15 20" para generar nuevos input de pruebas
"""

with open('dataset/sample_input.json', encoding='utf-8') as f:
    data_input = json.load(f)

ag_instancia = AlgoritmoGenetico()

ag_instancia.setup(porcentaje_cruza=0.5,
                   porcentaje_mut_ind=0.5,  # Porcentaje de mutación por indiviuo
                   porcentaje_mut_gen=0.5,  # Porcentaje de mutación por gen
                   poblacion_inicial=10,
                   poblacion_max=50,
                   generaciones=100
                   )

ag_instancia.load_preferences(data_input)
ag_instancia.run() # Empieza el ciclo de ejecución :)