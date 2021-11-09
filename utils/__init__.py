def str_fecha(tup, sep='-'):
    anno = tup[0]
    mes  = tup[1]
    dia  = tup[2]
    return f"{dia:02d}{sep}{mes:02d}{sep}{anno}"

def emoji_resultado(resultado):
    if resultado.lower() == "aprobado":
        return "✅"
    elif resultado.lower() == "rechazado":
        return "❌"
    return ""
    