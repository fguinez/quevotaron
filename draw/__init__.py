import os
if os.getcwd()[4:] == "draw":
    from main import generar_visualizaciones
else:
    from draw.main import generar_visualizaciones