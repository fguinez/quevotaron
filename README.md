# QueVotaron

- _**Nota:** Trabajo en proceso 🚧🚧🚧_

Proyecto destinado a visibilizar las votaciones de proyectos de ley del Congreso chileno por medio de visualizaciones autogeneradas de las votaciones.

Todas las visualizaciones son publicadas en nuestro Twitter:
<p align="center">
    <a href="https://twitter.com/quevotaron"><img src="https://imgur.com/hIXMqsE.png"> <b>@quevotaron</b></a>
</p>

## Por hacer

- Fusionar los módulos `api`, `handler` y `votaciones`. Actualmente `api` se encarga solo de realizar los requests y parsear a bs4 los HTML, mientras que `handler` y `votaciones` llaman a
los métodos de `api` para terminar de procesar la información. Esto podría considerarse un _code smell_ ([message chains](https://refactoring.guru/smells/message-chains)).
  - Hay dos posibles soluciones:
    1. Fusionar todo en un único archivo `api.py`
    2. Crear una carpeta `api` que contenga `diputados.py` y `votaciones.py`
- Implementar versión alternativa de `get_votaciones` para votaciones históricas (con diputados no vigentes)
  - Para ello es necesario utilizar la lista histórica de diputados, no la lista de diputados vigentes
  - Esto podría implicar desconocer quienes se ausentaron de la sala en ese momento
    - Posible solución: Filtrar los diputados vigentes al momento de votar por la fecha de votación


## Requisitos

Para instalar las librerías necesarias para correr el generador, ejecutar la siguiente línea en terminal:
```
pip install -r requirements.txt
```

## Aprendizajes

- **D3.js >>>>> PIL:** La generación de imágenes fue realizada con la librería PIL de Python, principalmente motivado por aprender una herramienta nueva. Sin embargo, el trabajo fue notoriamente más dificil y limitado que lo esperado, una mejor alternativa habría sido utilizar D3.js o alguna otra herramienta de edición vectorial.

## Guía de estilo

Este repositorio utiliza el idioma español tanto en su documentación como en el uso de `git flow`. Esto se fundamenta en el contexto chileno del proyecto QueVotaron, se busca facilitar y fomentar el uso nacional de la herramienta, por sobre un acceso universal tradicional. No está de más recordar que, en un proyecto de código abierto descontextualizado, sigue siendo una mejor práctica utilizar el idioma Inglés para la documentación.

En el caso de nombramiento de entidades se debe priorizar el uso de español, pero se permite la combinación de español con inglés ([_spanglish_](https://es.wikipedia.org/wiki/Espanglish)) cuando resulte más cómodo. Por ejemplo, es correcto llamar a una función `obtener_diputados`, pero también se permite `get_diputados` para simplificar las cosas.

Adicionalmente, se define el uso de commits atómicos con descripciones breves. Se recomienda comenzar los commits con un _emoji_ relacionado a su temática, seguido de una acción en presente.

Algunos ejemlos de commits válidos pueden ser:

- 🐛 Soluciona errores en el despliegue de diputados
- 📎 Adjunta imágenes de referencia en la carpeta de movimientos
- ✨ Implementa búsqueda binaria

Para un mayor detalle, se recomienda visitar [esta](https://gist.github.com/nebil/f96a2f0bfe1e059d589d6a2190a2ac81#file-styleguide-es-md) guía de estilo más completa.


## Referencias

- Datavizcatalogue. _Gráfico de Matriz de Puntos_. Ver [aquí](https://datavizcatalogue.com/ES/metodos/grafico_de_matriz_de_puntos.html).
  
- Unholster (Decide Chile). _Elección 2021: Constituyentes_. Ver [aquí](https://2021.decidechile.cl/#/ev/2021/ct/2021.N/)
