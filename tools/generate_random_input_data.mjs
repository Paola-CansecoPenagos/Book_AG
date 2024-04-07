/**
 * Genera datos de entrada aleatorios para entorno probar :)
 * usa node tools/generate_random_input_data.mjs <history> <categories> <authors>
 * Donde <history> corresponde a la cantidad de libros para añadir a historial, por defecto 10
 * Donde <categories> corresponde a la cantidad de categorias para añadir a favoritos, por defecto <history>
 * Donde <authors> corresponde a la cantidad de autores para añadir a favoritos, por defecto <categories>
 * Ejemplo:
 * node tools/generate_random_input_data.mjs 12 15 20
 */

const history_amount = process.argv.length >= 3 ?
    !isNaN(parseInt(process.argv[2])) ?
        parseInt(process.argv[2]) :
        10 :
    10;

const categories_amount = process.argv.length >= 4 ?
    !isNaN(parseInt(process.argv[3])) ?
        parseInt(process.argv[3]) :
        history_amount :
    history_amount;

const authors_amount = process.argv.length >= 5 ?
    !isNaN(parseInt(process.argv[4])) ?
        parseInt(process.argv[4]) :
        categories_amount :
    categories_amount;

import fs from 'fs'

import books from '../dataset/cleareddata.json' assert {type: 'json'}
import categories from '../dataset/categories.json' assert{type: 'json'}
import authors from '../dataset/authors.json' assert{type: 'json'}


function randGroup(cantidad, min, max) {

    let numeros = [];
    for (let i = min; i <= max; i++) {
        numeros.push(i);
    }

    if (cantidad > numeros.length) {
        console.error('La cantidad solicitada es mayor que la cantidad de números únicos disponibles.');
        return;
    }

    let numerosAleatorios = [];
    for (let i = 0; i < cantidad; i++) {
        const indiceAleatorio = Math.floor(Math.random() * numeros.length);
        numerosAleatorios.push(numeros.splice(indiceAleatorio, 1)[0]);
    }

    return numerosAleatorios;
}

const random_books_indexes = randGroup(history_amount, 0, books.length - 1)
const random_categories_indexes = randGroup(categories_amount, 0, categories.length - 1)
const random_author_indexes = randGroup(authors_amount, 0, authors.length - 1)

const categories_list = []
const authors_list = []
const history_list = []

random_books_indexes.map((ind, index) => {
    history_list.push(books[ind])
})

random_categories_indexes.map((ind, index) => {
    categories_list.push(categories[ind])
})

random_author_indexes.map((ind, index) => {
    authors_list.push(authors[ind])
})

const favorites = { categories: categories_list, authors: authors_list }

fs.writeFileSync('./dataset/sample_input.json', JSON.stringify({
    favorites: favorites,
    history: history_list
}, null, 4), 'utf8');