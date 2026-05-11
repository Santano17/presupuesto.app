import streamlit as st
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage

# =====================================================
# CONFIGURACIÓN APP
# =====================================================

st.set_page_config(
    page_title="Control Presupuesto y Albaranes",
    page_icon="💰",
    layout="wide"
)

# =====================================================
# LOGO EMPRESA
# =====================================================

st.image(
    "logo.png",
    width=350
)

st.title("💰 Control de Presupuesto y Albaranes")
st.subheader("SANTANO S.L. - OBRA ELÉCTRICA")

st.divider()

# =====================================================
# MEMORIA TEMPORAL
# =====================================================

if "registros_presupuesto" not in st.session_state:
    st.session_state.registros_presupuesto = []

if "registros_albaranes" not in st.session_state:
    st.session_state.registros_albaranes = []

# =====================================================
# PESTAÑAS
# =====================================================

tab1, tab2 = st.tabs([
    "💰 Seguimiento Presupuesto",
    "🧾 Albaranes"
])

# =====================================================
# TAB 1 - PRESUPUESTO
# =====================================================

with tab1:

    st.header("📋 Nuevo registro de presupuesto")

    numero_albaran = st.text_input(
        "🧾 Número de albarán",
        key="pres_albaran"
    )

    fecha = st.date_input(
        "📅 Fecha",
        value=date.today(),
        key="pres_fecha"
    )

    trabajador = st.text_input(
        "👷 Trabajador",
        key="pres_trabajador"
    )

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
        partidas,
        key="pres_partida"
    )

    gasto = st.number_input(
        "💸 Gastos de la partida (€)",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key="pres_gasto"
    )

    comentarios = st.text_area(
        "📝 Comentarios",
        height=120,
        key="pres_comentarios"
    )

    # =================================================
    # BOTÓN AÑADIR
    # =================================================

    if st.button(
        "➕ Añadir registro presupuesto"
    ):

        if numero_albaran.strip() == "":

            st.warning(
                "⚠️ Introduce el número de albarán"
            )

        elif trabajador.strip() == "":

            st.warning(
                "⚠️ Introduce el trabajador"
            )

        else:

            nuevo_registro = {
                "Número Albarán": numero_albaran.strip(),
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

    st.divider()

    st.subheader("📊 Registros presupuesto")

    df_presupuesto = pd.DataFrame(
        st.session_state.registros_presupuesto
    )

    if len(df_presupuesto) > 0:

        st.dataframe(
            df_presupuesto,
            use_container_width=True
        )

        total_gastos = df_presupuesto[
            "Gasto (€)"
        ].sum()

        st.metric(
            "💰 Total gastos",
            f"{total_gastos:.2f} €"
        )

        # =============================================
        # EXPORTAR EXCEL
        # =============================================

        nombre_excel_pres = (
            "seguimiento_presupuesto.xlsx"
        )

        df_presupuesto.to_excel(
            nombre_excel_pres,
            index=False
        )

        with open(
            nombre_excel_pres,
            "rb"
        ) as archivo:

            st.download_button(
                label="📥 Descargar Excel presupuesto",
                data=archivo,
                file_name=nombre_excel_pres,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:

        st.info(
            "No hay registros de presupuesto."
        )

# =====================================================
# TAB 2 - ALBARANES
# =====================================================

with tab2:

    st.header("🧾 Gestión de Albaranes")

    numero_albaran_tab2 = st.text_input(
        "🧾 Número de albarán",
        key="alb_numero"
    )

    fecha_albaran = st.date_input(
        "📅 Fecha albarán",
        value=date.today(),
        key="alb_fecha"
    )

    proveedor = st.text_input(
        "🏢 Proveedor",
        key="alb_proveedor"
    )

    descripcion = st.text_area(
        "📦 Descripción material",
        height=120,
        key="alb_descripcion"
    )

    importe = st.number_input(
        "💰 Importe (€)",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key="alb_importe"
    )

    observaciones = st.text_area(
        "📝 Observaciones",
        height=100,
        key="alb_observaciones"
    )

    # =================================================
    # BOTÓN AÑADIR ALBARÁN
    # =================================================

    if st.button(
        "➕ Añadir albarán"
    ):

        if numero_albaran_tab2.strip() == "":

            st.warning(
                "⚠️ Introduce el número de albarán"
            )

        elif proveedor.strip() == "":

            st.warning(
                "⚠️ Introduce el proveedor"
            )

        else:

            nuevo_albaran = {
                "Número Albarán": numero_albaran_tab2.strip(),
                "Fecha": fecha_albaran,
                "Proveedor": proveedor.strip(),
                "Descripción": descripcion.strip(),
                "Importe (€)": importe,
                "Observaciones": observaciones.strip()
            }

            st.session_state.registros_albaranes.append(
                nuevo_albaran
            )

            st.success(
                "✅ Albarán añadido correctamente"
            )

    st.divider()

    st.subheader("📋 Listado de albaranes")

    df_albaranes = pd.DataFrame(
        st.session_state.registros_albaranes
    )

    if len(df_albaranes) > 0:

        st.dataframe(
            df_albaranes,
            use_container_width=True
        )

        total_albaranes = df_albaranes[
            "Importe (€)"
        ].sum()

        st.metric(
            "💰 Total albaranes",
            f"{total_albaranes:.2f} €"
        )

        # =============================================
        # EXPORTAR EXCEL
        # =============================================

        nombre_excel_alb = (
            "albaranes.xlsx"
        )

        df_albaranes.to_excel(
            nombre_excel_alb,
            index=False
        )

        with open(
            nombre_excel_alb,
            "rb"
        ) as archivo:

            st.download_button(
                label="📥 Descargar Excel albaranes",
                data=archivo,
                file_name=nombre_excel_alb,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:

        st.info(
            "No hay albaranes registrados."
        )

# =====================================================
# EMAIL CONFIG
# =====================================================

EMAIL_REMITENTE = "tuemail@gmail.com"
PASSWORD_EMAIL = "abcdefghijklmnop"
EMAIL_DESTINO = "empresa@correo.com"

# =====================================================
# PIE FINAL
# =====================================================

st.divider()

st.caption(
    "© SANTANO S.L. - Sistema de control de presupuesto y albaranes."
)
