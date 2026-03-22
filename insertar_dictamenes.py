"""
Script de importación masiva de Dictámenes Técnicos
Fuente: G:\Mi unidad\2024_Dictamenes_Tecnicos_DT\
Destino: data/sistecdatos_dictamenes.db
Ejecutar desde el directorio raíz del proyecto:
    python insertar_dictamenes.py
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "sistecdatos_dictamenes.db")
if not os.path.exists(DB_PATH):
    # Intentar en la ruta raíz si no está en data/
    DB_PATH = os.path.join(os.path.dirname(__file__), "sigedta_dictamenes.db")
FECHA_IMPORTACION = datetime.now().strftime("%d/%m/%Y")
USUARIO = "admin"

DICTAMENES = [
    {
        "dictamen": "DT-011-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio Archaga, Municipio de Distrito Central, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF el 21 de noviembre de 2019 para revisar y decomisar "
            "expedientes de planes de saneamiento con presuntas irregularidades en su aprobación. "
            "Análisis técnico del Plan de Saneamiento RFFM-SA-010-2017 en Sitio Archaga."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "30/01/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "",
        "unidad": "",
    },
    {
        "dictamen": "DT-019-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "San Francisco, Municipio de Distrito Central, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF el 21 de noviembre de 2019 para revisar expedientes de planes de "
            "salvamento autorizados para control de plaga con presuntas irregularidades en su aprobación."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "13/02/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "",
        "unidad": "",
    },
    {
        "dictamen": "DT-024-2022",
        "denuncia": "De Oficio",
        "imputado": "Sociedad Mercantil Aserradero Monte Frescos S. de R.L.",
        "ofendido": "Estado de Honduras / Basilio Martínez Garmendia (propietario)",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "Cabeza de Vaca, entre Municipios de Morocelí y Teupasenti, Departamento de El Paraíso",
        "antecedentes": (
            "Inspecciones de junio y julio de 2021 por la UCTTI del ICF en El Encinal, Teupasenti, "
            "detectaron tala ilegal de bosques de pino fuera de los límites autorizados por resolución "
            "DE-MP-164-2020, sin consentimiento del propietario."
        ),
        "tecnico": "Fernando Ardón (Unidad Técnica Ambiental - FEMA)",
        "fecha": "04/02/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "",
        "unidad": "",
    },
    {
        "dictamen": "DT-024-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio Agua María Lote 2, Municipio de Cedros, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo del 21 de noviembre de 2019 en oficinas del ICF para revisar y decomisar "
            "expedientes de planes de salvamento con irregularidades en su aprobación. "
            "Análisis del Plan de Salvamento RFFM en Sitio Agua María."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "20/02/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "",
        "unidad": "",
    },
    {
        "dictamen": "DT-034-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "La Cofradía, Aldea El Círculo, Municipio de Ojojona, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF para revisar y decomisar expedientes de planes de "
            "saneamiento con irregularidades. Análisis técnico y evaluación de daños mediante "
            "teledetección e imágenes satelitales del Plan de Saneamiento RFFM-SA-010-2017."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "27/02/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Saneamiento RFFM-SA-010-2017",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-047-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio Pacaya, Municipio de Cantarranas, Departamento de Francisco Morazán",
        "antecedentes": (
            "Análisis del Plan de Salvamento ICF-RFFM-175-2017 en Sitio Pacaya. "
            "Se evaluó el aprovechamiento de madera de pino afectada por gorgojo (Dendroctonus frontalis) "
            "en 13.39 ha, con volumen total de 781.10 m³ de Pinus oocarpa."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "13/03/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan PSAL RFFM-175-2017",
        "unidad": "",
    },
    {
        "dictamen": "DT-049-2020",
        "denuncia": "1421179314-2015",
        "imputado": "Félix Julián Haddad, Oscar Suyanalof",
        "ofendido": "Teresa Andrews Searcy",
        "delito": "Corte y Aprovechamiento Ilegal de Productos Forestales",
        "sitio": "Colonia Menonita, Aldea Sabana Grande, Municipio de Guaimaca, Departamento de Francisco Morazán",
        "antecedentes": (
            "Denuncia por corte de madera en propiedad privada durante más de 3 años. "
            "Se encontraron árboles de pino marcados sin consentimiento de la denunciante "
            "Teresa Andrews Searcy en Colonia Menonita."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "22/07/2020",
        "fiscal": "Ismael Ordóñez (Fiscal de Medio Ambiente)",
        "agente": "Fausto Ramírez (UTA-FEMA), Ernesto Sánchez (PM), Javier Cruz (ICF)",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Expediente 1421095613-2015 acumulado",
        "unidad": "",
    },
    {
        "dictamen": "DT-055-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "La Pita, Municipio del Porvenir, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF para revisar y decomisar expedientes de planes de salvamento con "
            "irregularidades. Análisis de documentación y evaluación de daños mediante imágenes "
            "satelitales del Plan de Saneamiento RFFM-SA-100-2017."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "18/03/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Saneamiento RFFM-SA-100-2017",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-060-2024",
        "denuncia": "De Oficio",
        "imputado": "Ronald Valdéz Guevara, Cristian Fabricio Mejía",
        "ofendido": "El Medio Ambiente del Estado de Honduras",
        "delito": "Delitos Cometidos por Funcionarios Públicos / Explotación Ilegal de Recursos Naturales",
        "sitio": "Jícaro Galán, contiguo a la carretera panamericana CA-1, Municipio de Nacaome, Departamento de Valle",
        "antecedentes": (
            "Denuncia por descombro de árboles en Jícaro Galán. Se evidenció que no se había otorgado "
            "ni autorizado Plan de Salvamento. Se decomisó maquinaria pesada utilizada en el aprovechamiento ilegal."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "21/03/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "MAQUINARIA PESADA",
        "cantidad": "1",
        "otro": "Tractor Caterpillar D6D",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-069-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Los Pozos, Municipio de Talanga, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF para revisar y decomisar expedientes de planes de salvamento "
            "con irregularidades. Análisis técnico y evaluación de daños mediante teledetección e "
            "imágenes SIG. Plan de Salvamento RFFM-132-2016."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "09/04/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Salvamento RFFM-132-2016",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-085-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio Río Colorado, Municipio de Distrito Central, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF para revisar y decomisar expedientes de planes de salvamento "
            "con presuntas irregularidades. Análisis de documentación del Plan de Saneamiento "
            "RFFM-SA-010-2017 en Sitio Río Colorado."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "15/04/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Saneamiento RFFM-SA-010-2017",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-099-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Las Limas, Municipio de Distrito Central, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF para revisar y decomisar expedientes con presuntas irregularidades. "
            "Análisis del Plan de Salvamento ICF-RFFM-172-2016 aprobado a favor de José Reinaldo "
            "Moncada Silva para control de plaga de gorgojo en 7.3 hectáreas."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "03/05/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Salvamento ICF-RFFM-172-2016",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-115-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Cerro Cimartagua, Municipio de Lepaterique, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF para revisar y decomisar expedientes de planes de salvamento "
            "con presuntas irregularidades en su aprobación. Análisis técnico de la documentación "
            "del Plan de Salvamento en Cerro Cimartagua."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "27/05/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Salvamento - Cerro Cimartagua",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-119-2021",
        "denuncia": "1630597915-2021",
        "imputado": "Franklin Javier Hernández Cruz, Hong Chai Chang, Suyapa Vásquez de Chang",
        "ofendido": "El Equilibrio del Ecosistema / Estado de Honduras",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "Hacienda San Francisco, Municipio de Cedros, Departamento de Francisco Morazán",
        "antecedentes": (
            "Inspección del 28 de julio de 2021 reveló apertura de calle no autorizada, corte de árboles "
            "y utilización de bacadillas no autorizadas en el Plan Operativo 0942-002-1501-2021 "
            "de la Hacienda San Francisco."
        ),
        "tecnico": "Fernando Ardón (Sección Técnica Ambiental - FEMA)",
        "fecha": "18/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan Operativo 0942-002-1501-2021",
        "unidad": "",
    },
    {
        "dictamen": "DT-121-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Marale y Panal, Municipio de Marale, Departamento de Francisco Morazán",
        "antecedentes": (
            "Análisis del Plan de Salvamento RFFM-SA-038-2017 en los sitios Marale y Panal. "
            "Evaluación técnica con análisis de imágenes satelitales NDVI para verificar cumplimiento "
            "del plan de aprovechamiento forestal."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "03/06/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan RFFM-SA-038-2017",
        "unidad": "",
    },
    {
        "dictamen": "DT-127-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio El Bijagual, Municipio de Guaimaca, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF para revisar y decomisar expedientes de planes de salvamento con "
            "irregularidades. Plan ICF-RFFM-190-2016 aprobado a favor de la Municipalidad de "
            "Guaimaca para control de plagas de gorgojo en 12.76 hectáreas."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "10/06/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Salvamento ICF-RFFM-190-2016",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-147-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio El Bijagual (El Tigre), Municipio de Guaimaca, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF el 21 de noviembre de 2019 para revisar y decomisar expedientes de planes "
            "de salvamento con irregularidades. Análisis de plan de salvamento en Sitio El Bijagual "
            "con evaluación de imágenes satelitales y SIG."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "21/06/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expedientes de planes de salvamento decomisados en operativo ICF",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-149-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio El Bijagual Lote No. 4 - Los Izotes, Municipio de Talanga, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF para revisar y decomisar expedientes de planes de salvamento "
            "con presuntas irregularidades en su aprobación. Análisis de documentación del Plan de "
            "Salvamento RFFM-SA-313-2016 en Los Izotes."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez / Lucky Medina Estrada (Técnico Forestal ICF-Guaimaca)",
        "fecha": "27/06/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Salvamento RFFM-SA-313-2016",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-155-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Lologuara (Cañada de Flores), Municipio de Guaimaca, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF para revisar y decomisar expedientes de planes de salvamento "
            "con presuntas irregularidades. Análisis de documentación del Plan de Salvamento "
            "ICF-RFFM-012-2016 en Lologuara."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "24/07/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Salvamento ICF-RFFM-012-2016",
        "unidad": "Unidades",
    },
    {
        "dictamen": "DT-167-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio Hato Nuevo, Municipio de Talanga, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF el 21 de noviembre de 2019 para recuperar expedientes con irregularidades. "
            "Análisis del Plan de Salvamento ICF-RFFM-115-2016 en Hato Nuevo con verificación mediante "
            "imágenes satelitales y análisis NDVI."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "15/08/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan de Salvamento ICF-RFFM-115-2016",
        "unidad": "",
    },
    {
        "dictamen": "DT-169-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "La Peñita / La Mansión del Norte, Municipio de Guaimaca, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF para revisar expedientes irregulares. Análisis del Plan de Salvamento "
            "ICF-RFFM-174-2016 en La Mansión, Guaimaca, con verificación de área afectada por plaga "
            "de gorgojo mediante imágenes satelitales."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "19/08/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan de Salvamento ICF-RFFM-174-2016",
        "unidad": "",
    },
    {
        "dictamen": "DT-184-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio Casas Viejas, Municipio de Guaimaca, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF el 21 de noviembre de 2019 para decomisar expedientes irregulares. "
            "Análisis del Plan de Saneamiento ICF-RFFM-SA-030-2018 para control de plaga de gorgojo "
            "en Casas Viejas con verificación satelital."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "10/09/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan de Saneamiento ICF-RFFM-SA-030-2018",
        "unidad": "",
    },
    {
        "dictamen": "DT-190-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Sitio El Jícaro, Municipio de Ojojona, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en oficinas del ICF el 21 de noviembre de 2019 para revisar y decomisar "
            "expedientes de planes de salvamento con irregularidades en el Departamento de "
            "Francisco Morazán. Análisis técnico del sitio El Jícaro en Ojojona."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "23/09/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "",
        "unidad": "",
    },
    {
        "dictamen": "DT-215-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "San Isidro, Municipio de Distrito Central, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en ICF para revisar expedientes con irregularidades. Análisis del Plan de "
            "Saneamiento ICF-RFFM-SA-032-2018 para control de plaga de gorgojo en San Isidro, "
            "Distrito Central, con verificación satelital."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "07/09/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Plan de Saneamiento ICF-RFFM-SA-032-2018",
        "unidad": "",
    },
    {
        "dictamen": "DT-217-2024",
        "denuncia": "1559911646-2019",
        "imputado": "Romualdo Castillo, Denis Macoto, Edwin Alvarado y otros",
        "ofendido": "Administración Pública",
        "delito": "Abuso de Autoridad",
        "sitio": "Suyatal, Municipio de Distrito Central, Departamento de Francisco Morazán",
        "antecedentes": (
            "Operativo en las oficinas del ICF para revisar y decomisar expedientes del Plan de "
            "Saneamiento PSA-072-2018 con presuntas irregularidades en su aprobación. "
            "Análisis técnico mediante teledetección e imágenes satelitales."
        ),
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "14/10/2024",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "SI",
        "tipo": "OTROS",
        "cantidad": "1",
        "otro": "Expediente Plan de Saneamiento PSA-072-2018",
        "unidad": "Unidades",
    },
    # --- NUEVOS DICTÁMENES 2022 (IMPORTACIÓN DESDE G DRIVE) ---
    {
        "dictamen": "DT-025-2022",
        "denuncia": "Pendiente",
        "imputado": "Por determinar",
        "ofendido": "Estado de Honduras",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "KM4, Valle de Ángeles, Francisco Morazán",
        "antecedentes": "Inspección técnica y evaluación de daños en el sitio KM4, Valle de Ángeles.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: 2_DT_STA_FEMA_025_2022_KM4_VALLE_DE_ANGELES",
        "unidad": "",
    },
    {
        "dictamen": "APOYO-2022-04",
        "denuncia": "N/A",
        "imputado": "Varios",
        "ofendido": "Estado de Honduras",
        "delito": "Apoyo Técnico",
        "sitio": "Varios sitios",
        "antecedentes": "Documentación de apoyo técnico para diversas denuncias y operativos de 2022.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "04/04/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: 4_APOYOS",
        "unidad": "",
    },
    {
        "dictamen": "EXPORT-SPS-2022",
        "denuncia": "Exportación",
        "imputado": "Empresas Exportadoras",
        "ofendido": "Administración Pública",
        "delito": "Verificación de Análisis de Exportación",
        "sitio": "San Pedro Sula, Cortés",
        "antecedentes": "Análisis y verificación de exportaciones de productos forestales desde San Pedro Sula.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "05/05/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: 5_ANALASIS EXPORT SPS",
        "unidad": "",
    },
    {
        "dictamen": "DT-SITIO-SP-CATAMAS-06",
        "denuncia": "Pendiente",
        "imputado": "Por determinar",
        "ofendido": "Estado de Honduras",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "Sitio San Pedro de Catacamas, Olancho",
        "antecedentes": "Inspección y análisis técnico en Sitio San Pedro de Catacamas.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "06/06/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: 6_A_SITIO SAN PEDRO CATAMAS",
        "unidad": "",
    },
    {
        "dictamen": "NE-0298-001-0412-2018",
        "denuncia": "NE-0298-001-0412-2018",
        "imputado": "Nery Murillo",
        "ofendido": "Estado de Honduras",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "Gualaco, Olancho",
        "antecedentes": "Análisis de PM y POA en Gualaco según expediente NE-0298-001-0412-2018.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "12/04/2018",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: NE-0298-001-0412-2018_GUALACO",
        "unidad": "",
    },
    {
        "dictamen": "DT-JOHONNY-DUBON-MARAITA",
        "denuncia": "Pendiente",
        "imputado": "Johonny Dubon",
        "ofendido": "Estado de Honduras",
        "delito": "Delitos Forestales",
        "sitio": "Maraita, Francisco Morazán",
        "antecedentes": "Evaluación técnica de daños forestales en Maraita.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: JOHONNY_DUBON_MARAITA",
        "unidad": "",
    },
    {
        "dictamen": "DT-NOEMY-BRUNER-EL-HATILLO",
        "denuncia": "Pendiente",
        "imputado": "Noemy Bruner",
        "ofendido": "Estado de Honduras",
        "delito": "Corte Ilegal de Árboles",
        "sitio": "El Hatillo, Distrito Central, Francisco Morazán",
        "antecedentes": "Inspección técnica en El Hatillo por denuncia de corte ilegal.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: NOEMY_BRUNER_EL_HATILLO",
        "unidad": "",
    },
    {
        "dictamen": "DT-ASERRADERO-BORJAS",
        "denuncia": "Pendiente",
        "imputado": "Aserradero Borjas",
        "ofendido": "Administración Pública",
        "delito": "Verificación de Control Forestal",
        "sitio": "Aserradero Borjas",
        "antecedentes": "Inspección técnica y auditoría en Aserradero Borjas.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: ASERRADERO BORJAS",
        "unidad": "",
    },
    {
        "dictamen": "DT-CORRALITOS-2022",
        "denuncia": "Pendiente",
        "imputado": "Por determinar",
        "ofendido": "Estado de Honduras",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "Corralitos, Francisco Morazán",
        "antecedentes": "Inspección en la zona protegida o sitio de Corralitos.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: CORRALITOS",
        "unidad": "",
    },
    {
        "dictamen": "DT-JARAGUA-2022",
        "denuncia": "Pendiente",
        "imputado": "Por determinar",
        "ofendido": "Estado de Honduras",
        "delito": "Explotación Ilegal de Recursos Naturales",
        "sitio": "Jaragua",
        "antecedentes": "Inspección y evaluación en el sitio Jaragua.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía Especial de Medio Ambiente",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: Jaragua_2022",
        "unidad": "",
    },
    {
        "dictamen": "DT-FISCALIA-YUSCARAN-VERO",
        "denuncia": "Pendiente",
        "imputado": "Por determinar",
        "ofendido": "Estado de Honduras",
        "delito": "Delitos Ambientales",
        "sitio": "Yuscarán, El Paraíso",
        "antecedentes": "Apoyo a la Fiscalía de Yuscarán en caso relacionado con Vero.",
        "tecnico": "Fernando R. Ardón Rodríguez",
        "fecha": "01/01/2022",
        "fiscal": "Fiscalía de Yuscarán",
        "agente": "",
        "decomiso": "NO",
        "tipo": "",
        "cantidad": "",
        "otro": "Carpeta: VERO / FISCALIA_YUSCARAN",
        "unidad": "",
    },
]


def insertar_dictamenes():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: No se encontró la base de datos en: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    insertados = 0
    omitidos = 0
    errores = 0

    for d in DICTAMENES:
        try:
            # Verificar si ya existe
            cur.execute("SELECT dictamen FROM dictamenes WHERE dictamen = ?", (d["dictamen"],))
            existente = cur.fetchone()
            if existente:
                print(f"  [OMITIDO]  {d['dictamen']} — ya existe en la base de datos")
                omitidos += 1
                continue

            cur.execute(
                """
                INSERT INTO dictamenes (
                    dictamen, denuncia, imputado, ofendido, delito, sitio,
                    antecedentes, tecnico, fecha, fiscal, agente,
                    decomiso, tipo, cantidad, otro, unidad,
                    estado_dictamen, fecha_estado, entregado_a, fecha_entrega,
                    fecha_creacion, fecha_modificacion,
                    usuario_creacion, usuario_modificacion, activo
                ) VALUES (
                    :dictamen, :denuncia, :imputado, :ofendido, :delito, :sitio,
                    :antecedentes, :tecnico, :fecha, :fiscal, :agente,
                    :decomiso, :tipo, :cantidad, :otro, :unidad,
                    'Finalizado y entregado', :fecha, 'Fiscalía Especial de Medio Ambiente', :fecha,
                    :fecha_creacion, :fecha_creacion,
                    :usuario, :usuario, 1
                )
                """,
                {
                    **d,
                    "fecha_creacion": FECHA_IMPORTACION,
                    "usuario": USUARIO,
                },
            )
            conn.commit()
            print(f"  [OK]       {d['dictamen']} — {d['sitio'][:60]}")
            insertados += 1

        except sqlite3.IntegrityError as e:
            print(f"  [DUPLICADO] {d['dictamen']} — {e}")
            omitidos += 1
        except Exception as e:
            print(f"  [ERROR]    {d['dictamen']} — {e}")
            errores += 1

    conn.close()

    print()
    print("=" * 60)
    print(f"  Insertados : {insertados}")
    print(f"  Omitidos   : {omitidos}  (ya existían)")
    print(f"  Errores    : {errores}")
    print(f"  Total PDFs : {len(DICTAMENES)} registros únicos (de 28 PDFs fuente)")
    print("=" * 60)


if __name__ == "__main__":
    print(f"Base de datos: {DB_PATH}")
    print(f"Registros a importar: {len(DICTAMENES)}")
    print()
    insertar_dictamenes()
