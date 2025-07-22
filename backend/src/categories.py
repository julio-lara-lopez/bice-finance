diccionario_categorias_tc = {
    "SUPERMERCADO": ["unimarc", "lider", "jumbo", "tottus"],
    "INTERES": ["impuesto", "intereses", "comision"],
    "INTERNACIONAL": ["traspaso"],
    "INTERNET": ["movistar"],
    "PASAJES": ["latam", "despegar", "jetsmart", "sky"],
    "SALIDAS": ["uber eats", "floreria", "low free"],
    "CONSUMISMO": ["merpago venta", "zara", "paris"],
    "GYM": ["biogym", "sportlife", "budas"],
    "TRANSPORTE": ["uber trip", "cabify", "bip", "copec"],
    "SALUD": ["matfemaco", "salcrobrand", "cryz verde"],
    "SUSCRIPCION": ["prime video", "unicef", "disney", "hbo max"],
    "OTROS": []
}

diccionario_categorias_cc = diccionario_categorias_tc.copy()

def asignar_categoria(descripcion: str, diccionario: dict) -> str:
    descripcion = str(descripcion).lower()
    for categoria, keywords in diccionario.items():
        for keyword in keywords:
            if keyword in descripcion:
                return categoria
    return "OTROS"