import json

datos_limpios = []
ides = []

with open("dataset/sampledata.json", "r",  encoding="utf8") as f:
    datos = json.load(f)

for registro in datos:
    if (registro["id"] in ides):
        print("Saltando por repetición.")
        break

    ides.append(registro["id"])

    if "authors" in registro.get("volumeInfo", {}):
        autores = registro["volumeInfo"]["authors"]
    else:
        autores = ["Anónimo"]

    if "publishedDate" in registro.get("volumeInfo", {}):
        fecha_de_registro = registro["volumeInfo"]["publishedDate"]
    else:
        fecha_de_registro = "Sin información."

    if "imageLinks" in registro.get("volumeInfo", {}):
        imagen_uri = registro["volumeInfo"]["imageLinks"]["thumbnail"]
    else:
        imagen_uri = "#"

    if "categories" in registro.get("volumeInfo", {}):
        categorie = registro["volumeInfo"]["categories"]
    else:
        break  # No nos importa libros sin categoría.

    datos_limpios.append({
        "title": registro["volumeInfo"]["title"],
        "autores": autores,
        "fecha": fecha_de_registro,
        "imagen": imagen_uri,
        "categorias": categorie
    })

with open('dataset/cleareddata.json', 'w', encoding='utf-8') as archivo_salida:
    json.dump(datos_limpios, archivo_salida, indent=4, ensure_ascii=False)

print("Datos limpios guardados en cleareddata.json.")
