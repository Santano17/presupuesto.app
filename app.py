import streamlit as st
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage

# =====================================================
# CONFIGURACIÓN DE LA APP
# =====================================================

st.set_page_config(
    page_title="Seguimiento de Presupuesto",
    page_icon="💰",
    layout="centered"
)

# =====================================================
# LOGO EMPRESA
# =====================================================

st.image(
    "logo.png",
    width=350
)

# =====================================================
# TÍTULOS
# =====================================================

st.title("💰 Seguimiento de Presupuesto")
st.subheader("SANTANO S.L. - OBRA ELÉCTRICA")

st.divider()

# =====================================================
# MEMORIA TEMPORAL
# =====================================================

if "registros_presupuesto" not in st.session_state:
    st.session_state.registros_presupuesto = []

# =====================================================
# LISTADO DE ALBARANES
# =====================================================

albaranes = [
    "ALB-2026-001",
    "ALB-2026-002",
    "ALB-2026-003",
    "ALB-2026-004",
    "ALB-2026-005",
    "ALB-2026-006",
    "ALB-2026-007",
    "ALB-2026-008",
    "ALB-2026-009",
    "ALB-2026-010",
    "ALB-2026-011",
    "ALB-2026-012",
    "ALB-2026-013",
    "ALB-2026-014",
    "ALB-2026-015"
]

# =====================================================
# FORMULARIO
# =====================================================

st.header("📋 Nuevo registro")

numero_albaran = st.selectbox(
    "🧾 Selecciona el número de albarán",
    albaranes
)

fecha = st.date_input(
    "📅 Fecha",
    value=date.today()
)

trabajador = st.text_input(
    "👷 Trabajador"
)

# =====================================================
# PARTIDAS PRESUPUESTO
# =====================================================

partidas = [
    "Instalación eléctrica",
    "Cuadros eléctricos",
    "Iluminación",
    "Canalizaciones",
    "Cableado",
    "Automatización",
    "Domótica",
    "Puesta a tierra",
    "Protecciones eléctricas",
    "Mano de obra",
    "Material auxiliar",
    "Otros"
]

partida = st.selectbox(
    "📂 Partida del presupuesto",
    partidas
)

# =====================================================
# GASTOS
# =====================================================

gasto = st.number_input(
    "💸 Gastos de la partida (€)",
    min_value=0.0,
    step=0.01,
    format="%.2f"
)

# =====================================================
# COMENTARIOS
# =====================================================

comentarios = st.text_area(
    "📝 Comentarios",
    height=120
)

# =====================================================
# BOTÓN AÑADIR REGISTRO
# =====================================================

if st.button("➕ Añadir registro"):

    if trabajador.strip() == "":

        st.warning(
            "⚠️ Introduce el nombre del trabajador"
        )

    else:

        nuevo_registro = {
            "Número Albarán": numero_albaran,
            "Fecha": fecha,
            "Trabajador": trabajador.strip(),
            "Partida": partida,
            "Gasto (€)": gasto,
            "Comentarios": comentarios.strip()
        }

        st.session_state.registros_presupuesto.append(
            nuevo_registro
        )

        st.success(
            "✅ Registro añadido correctamente"
        )

# =====================================================
# MOSTRAR REGISTROS
# =====================================================

st.divider()

st.header("📊 Registros guardados")

df = pd.DataFrame(
    st.session_state.registros_presupuesto
)

if len(df) > 0:

    st.dataframe(
        df,
        use_container_width=True
    )

    # =================================================
    # TOTAL GASTOS
    # =================================================

    total_gastos = df["Gasto (€)"].sum()

    st.metric(
        label="💰 Total gastos acumulados",
        value=f"{total_gastos:.2f} €"
    )

else:

    st.info(
        "Todavía no hay registros."
    )

# =====================================================
# EXPORTAR A EXCEL
# =====================================================

nombre_excel = "seguimiento_presupuesto.xlsx"

if len(df) > 0:

    df.to_excel(
        nombre_excel,
        index=False
    )

    with open(nombre_excel, "rb") as archivo:

        st.download_button(
            label="📥 Descargar Excel",
            data=archivo,
            file_name=nombre_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# =====================================================
# CONFIGURACIÓN EMAIL
# =====================================================

EMAIL_REMITENTE = "nunezs.daniel@alumnos25.fundacionmasaveu.com"

PASSWORD_EMAIL = "zvbhfagykqjpjubo"

EMAIL_DESTINO = "ana@fundacionmasaveu.com"

# =====================================================
# FUNCIÓN ENVIAR EMAIL
# =====================================================

def enviar_email():

    remitente = str(
        EMAIL_REMITENTE
    ).strip()

    password = str(
        PASSWORD_EMAIL
    ).strip()

    # Soporta uno o varios correos
    if isinstance(EMAIL_DESTINO, list):

        destinatarios = [
            str(x).strip()
            for x in EMAIL_DESTINO
        ]

        destino_header = ", ".join(
            destinatarios
        )

    else:

        destinatarios = [
            str(EMAIL_DESTINO).strip()
        ]

        destino_header = destinatarios[0]

    # Crear email
    msg = EmailMessage()

    msg["Subject"] = (
        "Seguimiento de presupuesto"
    )

    msg["From"] = remitente

    msg["To"] = destino_header

    msg.set_content(
        "Adjunto Excel generado desde la app de seguimiento de presupuesto."
    )

    # Adjuntar Excel
    with open(nombre_excel, "rb") as f:

        contenido = f.read()

        msg.add_attachment(
            contenido,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=nombre_excel
        )

    # Conectar Gmail
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            remitente,
            password
        )

        smtp.send_message(msg)

# =====================================================
# BOTÓN ENVIAR EMAIL
# =====================================================

if len(df) > 0:

    if st.button("📧 Enviar Excel por correo"):

        try:

            enviar_email()

            st.success(
                "✅ Excel enviado correctamente"
            )

        except Exception as e:

            st.error(
                f"❌ Error enviando correo: {e}"
            )

# =====================================================
# PIE FINAL
# =====================================================

st.divider()

st.caption(
    "© SANTANO S.L. - Sistema de seguimiento y control de presupuesto."
)
