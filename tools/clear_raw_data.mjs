/**
 * Este script para limpiar y depurar datos de las colecciones en crudo del API
 */

import datas from '../dataset/raw.json' assert {type:'json'};
import fs from 'fs';

let id = 0;

const datosLimpios = [];
const ides = new Set();
const lista_categorias = new Set();
const lista_autores = new Set();

datas.map((data, index) => {
    if (ides.has(data.id)) {
        console.log("Saltando por repetición.");
        return;
    }

    ides.add(data.id);

    const autores = data.volumeInfo.authors || ["Anónimo"];
    const fechaDeRegistro = data.volumeInfo.publishedDate || "Sin información.";
    const imagenUri = (data.volumeInfo.imageLinks && data.volumeInfo.imageLinks.thumbnail) || "#";
    const categorias = data.volumeInfo.categories;

    if (!categorias) {
        console.log("No nos importa libros sin categoría.");
        return;
    }

    for (const categoria of categorias) {
        lista_categorias.add(categoria);
    }

    for (const autor of autores) {
        lista_autores.add(autor);
    }

    datosLimpios.push({
        id: ++id,
        title: data.volumeInfo.title,
        autores: autores,
        fecha: fechaDeRegistro,
        imagen: imagenUri,
        categorias: categorias
    });
});

fs.writeFileSync('./dataset/cleareddata.json', JSON.stringify(datosLimpios, null, 4), 'utf8');
fs.writeFileSync('./dataset/categories.json', JSON.stringify([...lista_categorias], null, 4), 'utf8');
fs.writeFileSync('./dataset/authors.json', JSON.stringify([...lista_autores], null, 4), 'utf8');

console.log("Datos limpios guardados en cleareddata.json.");