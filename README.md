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