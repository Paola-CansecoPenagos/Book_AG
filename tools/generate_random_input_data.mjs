/**
 * Genera datos de entrada aleatorios para entorno probar :)
 * usa node tools/generate_random_input_data.mjs 10
 * Donde 10 es el número de libros que se van a generar para crear el input falso.
 */

const amount_data_to_generate = parseInt(process.argv[process.argv.length - 1])

import data from '../dataset/cleareddata.json' assert {type: 'json'}
import fs from 'fs'

function generarNumerosAleatorios(cantidad, min, max) {

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

const random_indexes = generarNumerosAleatorios(amount_data_to_generate * 2, 0, data.length - 1)

const favorites = []
const history = []

random_indexes.map((ind, index)=>{
    if(index % 2){
        favorites.push(data[ind])
    }else{
        history.push(data[ind])
    }
})

fs.writeFileSync('./dataset/sample_input.json', JSON.stringify({
    favorites: favorites,
    history: history
}, null, 4), 'utf8');