from libs.AlgoritmoGenetico import AlgoritmoGenetico

ag_instancia = AlgoritmoGenetico()

ag_instancia.setup(porcentaje_cruza=0.5,
                   porcentaje_mut_ind=0.5,  # Porcentaje de mutación por indiviuo
                   porcentaje_mut_gen=0.5,  # Porcentaje de mutación por gen
                   poblacion_inicial=10,
                   poblacion_max=50,
                   generaciones=100
                   )

