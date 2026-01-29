# Config central: ciudades, nombres de hojas base, etc.

CITY_MAP = {
    "SC": ["SANTA CRUZ DE LA SIERRA", "SANTA CRUZ"],
    "CBBA": ["COCHABAMBA"],
    "LP": ["LA PAZ"],
    "EA": ["EL ALTO"],
    "OR": ["ORURO"],
    "PO": ["POTOSI", "POTOSÍ"],
    "SU": ["SUCRE"],
    "TJ": ["TARIJA"],
}

SHEET_REQ1 = "REQ.1-Demog."
SHEET_REQ2 = "REQ.2-Oport. (Base)"

# Por diseño:
# - REQ1/REQ2 se pegan en A2 sin headers (plantilla ya trae títulos)
# - SOVI/SECOS/EDF se pegan en A1 con headers (para asegurar títulos correctos)
ANCHORS = {
    "REQ": {"cell": "A2", "headers": False},
    "TT_CB": {"cell": "A2", "headers": False},
    "VAP": {"cell": "A2", "headers": False},
    "SOVI": {"cell": "A1", "headers": True},
    "SECOS": {"cell": "A1", "headers": True},
    "EDF": {"cell": "A1", "headers": True},
}

