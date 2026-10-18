import streamlit as st
import random
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Proyecto Ataraxia | WoW TDAH System", page_icon="⚔️", layout="centered")

SAVE_FILE = "ataraxia_save.json"
PERU_TZ = ZoneInfo("America/Lima")

# --- BASE DE DATOS DEL SISTEMA ---
RANKS = [
    (0, "Iniciado Escarlata", "Set de Tela Gris + Maza de Madera Desgastada", "Personalizar el tema visual de tu entorno de trabajo."),
    (50, "El Paciente", "Set de Malla de Cobre + Escudo Abollado", "Comprar una cajetilla de hojas de afeitar de doble filo nuevas (Feather/Astra)."),
    (120, "Explorador", "Placas de Mithril + Espada Ancha de Hierro", "Comprar cuerdas nuevas o selección de púas para la guitarra."),
    (220, "Campeón de la Ciudadela", "Set de Valor (Tier 0.5) + Escudo de Roca Negra", "Comprar 250g de café de especialidad para las tardes."),
    (340, "Justicar", "Set de Sentencia (Tier 2) + Baluarte de Azzinoth", "Bloque de 3 horas de domingo libre (WoW, Dota 2 o RDR2) sin culpa."),
    (480, "Mano de A'dal", "Set de Portador de Luz (Tier 6) + Espada del Vacío", "Adquirir un jabón/crema de afeitar clásica nueva o piedra de alumbre."),
    (640, "Cruzado Argenta", "Set de Triunfo (Tier 9H) + Baluarte del Rey Exánime", "Juguete/lata gourmet para tus gatos + tarde de básquet sin reloj."),
    (820, "El Indestructible", "Set de Jurapenas (Tier 10) + Muro Glacial", "Comprar un libro físico o magnesio/bandas para calistenia."),
    (1020, "Matarreyes", "Tier 10 Santificado + Mithrios, legado de Barbabronce", "Cena de corte de carne magra / parrilla limpia."),
    (1250, "Luz del Alba", "Tier 10 Heroico (277) + Crematoria (Ashbringer)", "Adquirir una brocha de afeitar superior o herramienta para tu setup."),
    (1500, "El Iluminado", "BiS Transfigurado + Crematoria Corrupta", "Retiro del Emperador: 24 horas libres haciendo lo que te plazca."),
    (1800, "El Loco de Amor", "Set de Redención + Trueno Furioso, espada bendita del Hijo del Viento", "BOTÍN LEGENDARIO: Artículo insignia de colección (afeitado clásico, guitarra o hardware).")
]

MODIFIERS_0M = [
    "Voto de Silencio: Habla solo lo estrictamente indispensable en el hospital y la UCSM. Cero charla trivial.",
    "Modo Hardcore: Cero uso del celular durante tus viajes en carro (1h) y caminatas (35m).",
    "Postura del Tanque: Espalda recta y hombros atrás cada segundo que lleves puesto el uniforme médico.",
    "Banda Sonora de Época: Escucha un álbum completo de Frank Sinatra, Fred Astaire o Laufey en orden, sin saltar pistas.",
    "Aversión al Azúcar: Cero bebidas azucaradas, postres o snacks procesados hoy. Solo agua, café negro o té.",
    "Mano Izquierda Dominante: Abre puertas, usa el mouse o carga objetos con tu mano no dominante todo el día.",
    "Filtro Marco Aurelio: Prohibido emitir quejas verbales o mentales sobre el tráfico, EsSalud o la universidad.",
    "Escaneo Táctico: Al entrar a cualquier sala o laboratorio, identifica en 5 segundos salidas y dinámicas de poder.",
    "Pulso Rítmico: En el carro, lleva el compás con la mano derecha (rumba flamenca o huayno) de todo lo que escuches.",
    "Hidratación de Asedio: Toma un vaso grande de agua al salir de casa, llegar al hospital, llegar a la UCSM y volver.",
    "Telegrama Clínico: En chats no urgentes, responde usando máximo 8 palabras por mensaje hoy.",
    "Impecabilidad de Gala: Mantén tu uniforme médico sin una sola arruga ni mancha hasta regresar a casa.",
    "Pensamiento Bilingüe: Estructura tus pendientes y reflexiones mentales exclusivamente en inglés académico en ruta.",
    "Respiración Nasal Estricta: Durante los 70 min totales de caminata, respira única y exclusivamente por la nariz.",
    "Bloqueo de Dopamina Barata: Cero Reels, TikTok o Shorts hasta haber completado el banco de preguntas de hoy."
]

QUESTS_30M = [
    "Ruta de Evasión (30 min): Camina de la UCSM al paradero por calles del Centro que no hayas pisado este mes.",
    "Tensión Isométrica (30 min): Encuentra un parque en tu ruta y haz 3 series al fallo de dead hangs o pull-ups negativas con uniforme.",
    "Censo Felino (30 min): Encuentra, observa y fotografía a 3 gatos distintos en tu caminata hacia el paradero.",
    "Arquitectura en Tránsito (30 min): En el carro, diseña en notas el flujo lógico de un nuevo script de Python/Streamlit para Omipro Core.",
    "Banco Relámpago (30 min): Resuelve 25 preguntas de EsSalud en el celular durante el viaje en carro.",
    "Marcha Forzada (30 min): Completa la caminata de 35 min de la UCSM al paradero en menos de 26 minutos.",
    "Cata de Café Oculto (30 min): Entra a una cafetería pequeña del centro que no conozcas por un espresso/americano (máx S/ 8).",
    "Auditoría Comercial (30 min): Caminando al paradero, analiza 3 locales con poca clientela y deduce por qué fallan.",
    "Peer Review en Movimiento (30 min): Descarga un paper Q1 reciente y audita su metodología y figuras en el carro.",
    "Observación de NPCs (30 min): Elige 3 transeúntes y deduce su profesión, origen y ánimo solo por su calzado y postura.",
    "Duelo de Memoria Clínica (30 min): De camino a la UCSM, recita mentalmente la fisiopatología de 2 casos vistos en la mañana.",
    "Disección Acústica (30 min): Escucha 3 piezas de Savia Andina, Bossa Nova o Jazz y desglosa la guitarra base mentalmente.",
    "Inbox Zero en Ruta (30 min): Usa la mitad del viaje en carro para limpiar fotos basura, descargas y correos pendientes.",
    "Isometría Oculta (30 min): En el carro, haz 10 series de stomach vacuum (20s) y ejercicios de movilidad de dedos para guitarra."
]

QUESTS_1H = [
    "Cacería de Reliquias (1 hora): Entra a tiendas de antigüedades en el centro buscando navajas o safety razors. Prohibido comprar, solo tasar.",
    "Oído Absoluto (1 hora): Saca de oído en guitarra un huayno puneño o rumba flamenca sin mirar acordes en internet.",
    "Simulación de Crisis (1 hora): Diseña un plan para Omipro Core asumiendo que debes facturar 100% en el extranjero desde mañana.",
    "Laboratorio de Crossover (1 hora): Ve a una cancha de básquet a practicar bote, crossovers y 50 tiros libres/bandejas en solitario.",
    "Refactorización Implacable (1 hora): Toma un script antiguo de R o Python del laboratorio y reduce sus líneas a la mitad.",
    "Mantenimiento de Arsenal (1 hora): Desinfecta y pule tu safety razor, hidrata el diapasón de tu guitarra y ordena tu escritorio al milímetro.",
    "Ingeniería Felina (1 hora): Construye un circuito/juguete casero para tus dos gatos y juega con ellos sin mirar el celular.",
    "Infiltración Académica (1 hora): Entra a un pabellón o biblioteca de la UCSM que nunca uses y estudia ahí 1 hora seguida.",
    "Exploración Estructural (1 hora): Abre PyMOL o ColabFold por 1 hora y modela una proteína rara por pura curiosidad científica.",
    "Bloque de Fuerza Estricta (1 hora): Haz progresiones de pull-ups (escapulares, australian rows, negativas de 10s) cronometrando descansos.",
    "Theorycrafting del Offlane (1 hora): Analiza matchups y estadísticas de un Pos 3 (Dark Seer, NS, Brewmaster) y crea una build matemática sin jugar.",
    "Caminata del Fantasma (1 hora): Camina por San Lázaro, Yanahuara o el Chili sin audífonos, registrando arquitectura histórica."
]

DAILY_REWARDS = [
    "🎮 Caza Mayor en RDR2: 45 min libres para cazar animales legendarios o pescar con Arthur Morgan.",
    "🛡️ Dominio del Offlane: 1 partida de Dota 2 en Posición 3 jugando el héroe que prefieras.",
    "⚔️ Tanqueo en Rasganorte: 1 hora de WoW 3.3.5a con tu Paladín Protección.",
    "🪒 Ritual de Barbería Clásica: Afeitado nocturno con toalla caliente, espuma en tazón y loción post-afeitado.",
    "☕ Elixir de Especialidad: Preparar o comprar un café negro de especialidad o té importado.",
    "🎸 Sesión Acústica Libre: 45 min tocando tus temas favoritos en guitarra a todo volumen.",
    "🐈 Ataraxia con Gatos y Jazz: 30 min escuchando Sinatra/Laufey con tus gatos, prohibido pensar en medicina.",
    "📺 Archivo Clasificado: 1 episodio de La Gran Sangre o documental de lore (Half-Life / StarCraft / WoW).",
    "🥩 Snack Proteico de Autor: Preparar un snack salado alto en proteína y bajo en calorías.",
    "🪙 Micro-Adquisición (< S/ 5): Comprar una púa de guitarra nueva o un agua con gas helada con limón.",
    "🚀 Partida RTS Relámpago: 40 min de StarCraft II para entrenar velocidad de decisiones.",
    "🛌 Pase de Sueño Táctico: Siesta de 25 min en la tarde o dormir 45 min antes hoy."
]

# --- FUNCIONES DE PERSISTENCIA Y LÓGICA BLINDADAS ---
def get_default_state():
    return {
        "ilvl": 0,
        "last_date": "",
        "daily_mod": "",
        "daily_quest": "",
        "daily_quest_type": "",
        "daily_reward": "",
        "completed_quest": False,
        "completed_essalud": False,
        "completed_omipro": False,
        "rerolls_left": 1
    }

def load_data():
    today_str = str(datetime.now(PERU_TZ).date())
    data = get_default_state()
    
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    loaded = json.loads(content)
                    if isinstance(loaded, dict):
                        data.update(loaded)
        except (json.JSONDecodeError, OSError):
            # Si el archivo está vacío o corrupto, usa el estado base y lo sobrescribe abajo
            pass
    
    if data["last_date"] != today_str or not data["daily_quest"]:
        roll_new_day(data, today_str)
    return data

def save_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def roll_new_day(data, today_str):
    data["last_date"] = today_str
    data["daily_mod"] = random.choice(MODIFIERS_0M)
    if random.random() < 0.65:
        data["daily_quest"] = random.choice(QUESTS_30M)
        data["daily_quest_type"] = "Reto de Ruta (30 min)"
    else:
        data["daily_quest"] = random.choice(QUESTS_1H)
        data["daily_quest_type"] = "Evento Fuera de Ruta (1 hora)"
    data["daily_reward"] = random.choice(DAILY_REWARDS)
    data["completed_quest"] = False
    data["completed_essalud"] = False
    data["completed_omipro"] = False
    data["rerolls_left"] = 1
    save_data(data)

def get_current_rank(ilvl):
    current = RANKS[0]
    next_rank = None
    for i, r in enumerate(RANKS):
        if ilvl >= r[0]:
            current = r
            next_rank = RANKS[i + 1] if i + 1 < len(RANKS) else None
    return current, next_rank

# --- INTERFAZ PRINCIPAL ---
data = load_data()
current_rank, next_rank = get_current_rank(data["ilvl"])

st.title("⚔️ Proyecto Ataraxia: Panel de Control")
st.caption(f"Fecha Operativa (Perú): {data['last_date']} | Clase: Paladín Protección / Científico-Empresario")

# --- FICHA DE PERSONAJE (GEARSCORE) ---
st.subheader(f"👑 Título Actual: *{current_rank[1]}*")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="GearScore (iLvl)", value=f"{data['ilvl']} iLvl")
with col2:
    st.markdown(f"**Equipamiento Activo:**\n`{current_rank[2]}`")

if next_rank:
    progress = (data["ilvl"] - current_rank[0]) / (next_rank[0] - current_rank[0])
    st.progress(min(max(progress, 0.0), 1.0))
    st.caption(f"Faltan **{next_rank[0] - data['ilvl']} iLvl** para desbloquear: **{next_rank[1]}** ({next_rank[2]})")
else:
    st.progress(1.0)
    st.success("⚡ HAS ALCANZADO EL RANGO MÁXIMO: EL LOCO DE AMOR. EMPUÑAS A TRUENO FURIOSO.")

st.divider()

# --- MISIONES DEL DÍA ---
st.subheader("📜 Matriz de Retos de Hoy")
st.info(f"**🛡️ Modificador Pasivo (0 min - Todo el día):**\n\n{data['daily_mod']}")
st.warning(f"**⚡ {data['daily_quest_type']} (Exclusivo):**\n\n{data['daily_quest']}")

if data["rerolls_left"] > 0 and not data["completed_quest"]:
    if st.button(f"🪨 Usar Piedra de Hogar (Reroll de Misión - Quedan {data['rerolls_left']})"):
        if random.random() < 0.65:
            data["daily_quest"] = random.choice(QUESTS_30M)
            data["daily_quest_type"] = "Reto de Ruta (30 min)"
        else:
            data["daily_quest"] = random.choice(QUESTS_1H)
            data["daily_quest_type"] = "Evento Fuera de Ruta (1 hora)"
        data["rerolls_left"] -= 1
        save_data(data)
        st.rerun()

st.divider()

# --- REGISTRO DE EJECUCIÓN Y RECOMPENSAS ---
st.subheader("🎯 Registro de Ejecución Diaria")

c1, c2, c3 = st.columns(3)
with c1:
    if not data["completed_quest"]:
        if st.button("✅ Completar Reto (+25 iLvl)"):
            data["ilvl"] += 25
            data["completed_quest"] = True
            save_data(data)
            st.balloons()
            st.rerun()
    else:
        st.success("Reto Completado (+25)")

with c2:
    if not data["completed_essalud"]:
        if st.button("📚 2h Banco EsSalud (+20 iLvl)"):
            data["ilvl"] += 20
            data["completed_essalud"] = True
            save_data(data)
            st.rerun()
    else:
        st.success("EsSalud Completado (+20)")

with c3:
    if not data["completed_omipro"]:
        if st.button("🧬 Avance Omipro/Lab (+15 iLvl)"):
            data["ilvl"] += 15
            data["completed_omipro"] = True
            save_data(data)
            st.rerun()
    else:
        st.success("Omipro/Lab Completado (+15)")

# --- BOTÍN DIARIO DESBLOQUEADO ---
st.divider()
st.subheader("🎁 Bóveda de Recompensas")

if data["completed_quest"] or data["completed_essalud"]:
    st.success(f"**[BOTÍN DIARIO DESBLOQUEADO]:**\n\n### {data['daily_reward']}")
else:
    st.error("🔒 **Botín Diario Bloqueado:** Completa el Reto del Día o tus 2 horas de Banco EsSalud para revelar y reclamar tu recompensa de hoy.")

# --- LOGROS Y RECOMPENSAS DE RANGO ---
with st.expander("🏆 Ver Recompensas de Hito Desbloqueadas (Logros de GearScore)"):
    for r_ilvl, r_title, r_gear, r_reward in RANKS:
        if data["ilvl"] >= r_ilvl:
            st.markdown(f"✅ **{r_title} ({r_ilvl} iLvl):** {r_reward} *(Equipo: {r_gear})*")
        else:
            st.markdown(f"🔒 *{r_title} ({r_ilvl} iLvl): Bloqueado*")

# --- SIDEBAR: BACKUP Y CONTROL ---
with st.sidebar:
    st.header("⚙️ Sistema y Respaldo")
    st.download_button(
        label="💾 Descargar Partida (JSON)",
        data=json.dumps(data, ensure_ascii=False, indent=4),
        file_name="ataraxia_save.json",
        mime="application/json"
    )
    uploaded_file = st.file_uploader("📂 Restaurar Partida (JSON)", type=["json"])
    if uploaded_file is not None:
        try:
            restored_data = json.load(uploaded_file)
            save_data(restored_data)
            st.success("Partida actualizada.")
            if st.button("Aplicar Recarga"):
                st.rerun()
        except json.JSONDecodeError:
            st.error("El archivo subido no es un JSON válido.")
