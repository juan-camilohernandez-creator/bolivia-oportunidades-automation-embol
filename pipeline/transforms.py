import pandas as pd
import re

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia BOM y espacios en nombres de columnas (clásico en CSVs)."""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )
    return df

def get_col(df: pd.DataFrame, target_lower: str):
    """Encuentra una columna por nombre en minúscula (robusto)."""
    cols = {str(c).replace("\ufeff", "").strip().lower(): c for c in df.columns}
    return cols.get(target_lower)

def norm_group(x):
    if pd.isna(x): 
        return x
    s = re.sub(r"\s+", " ", str(x).strip().upper())
    if "TRADIC" in s:
        return "TRADICIONAL"
    if ("COMER" in s and "BEB" in s) or ("COMER Y BEBER" in s) or ("COMER & BEBER" in s):
        return "COMER & BEBER"
    return s

def norm_city(x):
    if pd.isna(x): 
        return x
    return re.sub(r"\s+", " ", str(x).strip().upper())

def filter_by_city(df: pd.DataFrame, city_list):
    col_city = get_col(df, "ciudad")
    if not col_city:
        raise ValueError(f"No encontré columna Ciudad/ciudad. Columnas: {list(df.columns)}")
    out = df.copy()
    out["_city"] = out[col_city].map(norm_city)
    city_list = [norm_city(x) for x in city_list]
    out = out[out["_city"].isin(city_list)]
    return out.drop(columns=["_city"], errors="ignore")

def filter_by_canal(df: pd.DataFrame, canal_value: str):
    col_canal = get_col(df, "canal")
    if not col_canal:
        raise ValueError(f"No encontré columna Canal/canal. Columnas: {list(df.columns)}")
    out = df.copy()
    out = out[out[col_canal].astype(str).str.strip().str.upper() == canal_value.strip().upper()]
    return out

def filter_presencias_by_group_city(df: pd.DataFrame, grupo: str, cities):
    """Filtra presencias por Grupo_Canal + Ciudad."""
    out = df.copy()
    col_gc = get_col(out, "grupo_canal")
    col_city = get_col(out, "ciudad")
    if not col_gc or not col_city:
        raise ValueError("Presencias debe tener Grupo_Canal y Ciudad.")

    out["_gc"] = out[col_gc].map(norm_group)
    out["_city"] = out[col_city].map(norm_city)

    out = out[out["_gc"] == grupo]
    out = out[out["_city"].isin([norm_city(x) for x in cities])]
    return out.drop(columns=["_gc", "_city"], errors="ignore")

def transform_edf_final(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte flags EDF a columnas finales Invasion y Tipo Invasion, y deja el orden requerido."""
    df = clean_columns(df)

    invasion_cols = ["invasion_5_or_less", "invasion_6_12", "invasion_12_24", "invasion_more_than_24"]
    tipo_cols = ["alcoholic_beverages", "competitor_products", "other_products"]
    invasion_cols = [c for c in invasion_cols if c in df.columns]
    tipo_cols = [c for c in tipo_cols if c in df.columns]

    invasion_map = {
        "invasion_5_or_less": "5 o menos",
        "invasion_6_12": "Entre 6 y 12",
        "invasion_12_24": "Entre 12 y 24",
        "invasion_more_than_24": "Mas de 24",
    }
    tipo_map = {
        "alcoholic_beverages": "Bebidas Alcoholicas",
        "competitor_products": "Productos de la competencia",
        "other_products": "Otros Productos",
    }

    def pick_hits(row, cols, mapping, default=None):
        hits = []
        for c in cols:
            v = row.get(c)
            if pd.isna(v):
                continue
            if str(v).strip() in ("1", "1.0", "TRUE", "True", "true"):
                hits.append(mapping.get(c, c))
        return ", ".join(hits) if hits else default

    df["Invasion"] = df.apply(lambda r: pick_hits(r, invasion_cols, invasion_map, default="Sin Invasion"), axis=1)
    df["Tipo Invasion"] = df.apply(lambda r: pick_hits(r, tipo_cols, tipo_map, default=None), axis=1)

    df.drop(columns=invasion_cols + tipo_cols, inplace=True, errors="ignore")

    desired_order = [
        "place_id", "Ciudad", "qr_code", "Fecha", "canal", "channel_group",
        "Codigo_cliente_Embol", "place_name", "ruta_kof", "lat", "lon",
        "operacion", "my_cooler_invaded", "Invasion", "Tipo Invasion",
    ]
    existing = [c for c in desired_order if c in df.columns]
    extras = [c for c in df.columns if c not in existing]
    return df[existing + extras]

