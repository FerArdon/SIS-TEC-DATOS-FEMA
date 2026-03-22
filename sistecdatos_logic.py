# sistecdatos_logic.py
import sqlite3
import logging
import os
from sistecdatos_i18n import _

logger = logging.getLogger("sistecdatos.logic")

# Diccionario centralizado de tipos y unidades (movido de main.py)
TIPOS_DECOMISO = {
    "MADERA EN ROLLO": {"unidad": "m³", "categoria": "Forestal"},
    "MADERA ASERRADA": {"unidad": "PT", "categoria": "Forestal"},
    "LEÑA": {"unidad": "Cargas", "categoria": "Forestal"},
    "ASERRÍN": {"unidad": "Tonelada métrica", "categoria": "Forestal"},
    "CARBÓN VEGETAL": {"unidad": "Sacos", "categoria": "Forestal"},
    "MATERIAL MINERÍA": {"unidad": "Toneladas", "categoria": "Minero"},
    "SUELO CONTAMINADO": {"unidad": "Toneladas", "categoria": "Suelo"},
    "AGUA CONTAMINADA": {"unidad": "Litros", "categoria": "Agua"},
    "FAUNA SILVESTRE": {"unidad": "Unidades", "categoria": "Fauna"},
    "FLORA SILVESTRE": {"unidad": "Unidades", "categoria": "Flora"},
    "EMISIONES AIRE": {"unidad": "m³", "categoria": "Aire"},
    "MAQUINARIA PESADA": {"unidad": "Unidades", "categoria": "Forestal"},
    "EQUIPO FORESTAL": {"unidad": "Unidades", "categoria": "Forestal"},
    "EQUIPO MINERO": {"unidad": "Unidades", "categoria": "Minero"},
    "PRODUCTOS QUÍMICOS": {"unidad": "Libras", "categoria": "Químico"},
    "OTROS": {"unidad": "", "categoria": "Otro"},
}

TIPOS_OPCIONES = list(TIPOS_DECOMISO.keys())

CAMPOS_DICTAMEN = [
    "dictamen", "denuncia", "imputado", "ofendido", "delito", "sitio",
    "antecedentes", "tecnico", "fecha", "fiscal", "agente", "decomiso",
    "tipo", "cantidad", "otro", "unidad", "estado_dictamen", "fecha_estado",
    "entregado_a", "fecha_entrega"
]

class SISTECDATOSFEMALogic:
    """Capa de lógica de negocio para separar la UI de la BD."""
    
    def __init__(self, db_manager):
        self.db = db_manager

    def validar_campos(self, campos: dict, formato_fecha: str) -> tuple:
        """Valida campos obligatorios y formatos."""
        obligatorios = ["dictamen", "denuncia", "delito", "tecnico"]
        for c in obligatorios:
            if not campos.get(c):
                return False, (c, _("campo_obligatorio", campo=_(c)))
        
        # Validar formato de fecha si se provee
        from datetime import datetime
        fechas = ["fecha", "fecha_estado"]
        for f in fechas:
            if campos.get(f):
                try:
                    datetime.strptime(campos[f], formato_fecha)
                except ValueError:
                    return False, (f, f"Formato de fecha inválido para {_(f)}")
        
        return True, None

    def validar_estado_entrega(self, estado, entregado_a, fecha_entrega, estado_entregado) -> tuple:
        """Valida que si el estado es 'Entregado', existan los datos correspondientes."""
        if estado == estado_entregado:
            if not entregado_a or not fecha_entrega:
                return False, ("entregado_a", "Si el dictamen está entregado, debe indicar a quién y en qué fecha.")
        return True, None

    def guardar_dictamen(self, campos: dict):
        """Prepara y guarda el dictamen en la BD."""
        # Convertir dict a lista ordenada para el insert_dictamen de la BD
        fila = [campos.get(k, "") for k in CAMPOS_DICTAMEN]
        self.db.insert_dictamen(fila)
        logger.info(f"Dictamen '{campos.get('dictamen')}' guardado exitosamente.")

    def eliminar_dictamen(self, dictamen_num):
        """Elimina un dictamen."""
        self.db.delete_dictamen(dictamen_num)
        logger.info(f"Dictamen '{dictamen_num}' eliminado (borrado lógico).")

    def cargar_pagina(self, pagina, size, search_query=""):
        """Carga datos paginados."""
        offset = pagina * size
        total = self.db.count_dictamenes(search_query)
        rows = self.db.fetch_dictamenes_paginados(offset=offset, limit=size, search_query=search_query)
        return rows, total, pagina

    def guia_tipos(self):
        """Genera el texto para la guía de tipos."""
        return "\n".join([f"{k}: unidad {v['unidad']} ({_(v['categoria'].lower())})" for k, v in TIPOS_DECOMISO.items()])

    def obtener_categoria_para_tipo(self, tipo):
        return TIPOS_DECOMISO.get(tipo, {}).get("categoria", "Otro")

    def obtener_unidades_para_tipo(self, tipo):
        """Retorna las unidades sugeridas para un tipo."""
        if tipo == "OTROS":
            return ["Unidades", "Piezas", "Kilogramos", "Libras", "m³", "PT", "Cargas", "Litros", "Galones"]
        return [TIPOS_DECOMISO.get(tipo, {}).get("unidad", "")]

    def tipo_permite_unidad_libre(self, tipo):
        return tipo == "OTROS"
