# QueVotaron
Proyecto destinado a visibilizar las votaciones de proyectos de ley del Congreso chileno.

## Por hacer

- Implementar versión alternativa de `get_votaciones` para votaciones históricas (con diputados no vigentes)
  - Para ello es necesario utilizar la lista histórica de diputados, no la lista de diputados vigentes
  - Esto podría implicar desconocer quienes se ausentaron de la sala en ese momento
    - Posible solución: Filtrar los diputados vigentes al momento de votar por la fecha de votación

- Diseñar plantilla de imagen

- Automatizar mapeo de resultados a imagen


## Requisitos

Para instalar las librerías necesarias para correr el generador, ejecutar la siguiente línea en terminal:
```
pip install -r requirements.txt
```

## Guía de estilo

Este repositorio utiliza el idioma español tanto en su documentación como en el uso de `git flow`. Esto se fundamenta en el contexto chileno del proyecto QueVotaron, se busca facilitar y fomentar el uso nacional de la herramienta, por sobre un acceso universal tradicional. No está de más recordar que, en un proyecto de código abierto descontextualizado, sigue siendo una mejor práctica utilizar el idioma Inglés para la documentación.

Adicionalmente, se define el uso de commits atómicos con descripciones breves. Se recomienda comenzar los commits con un _emoji_ relacionado a su temática, seguido de una acción en presente.

Algunos ejemlos de commits válidos pueden ser:

- 🐛 Soluciona errores en el despliegue de diputados
- 📎 Adjunta imágenes de referencia en la carpeta de movimientos
- ✨ Implementa búsqueda binaria

Para un mayor detalle, se recomienda visitar [esta](https://gist.github.com/nebil/f96a2f0bfe1e059d589d6a2190a2ac81#file-styleguide-es-md) guía de estilo más completa.