import streamlit as st
from pipeline.runner import build_workbook_bytes

st.set_page_config(
    page_title="Automatización Oportunidades Bolivia",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Automatización Oportunidades Bolivia")
st.caption("Carga 5 CSV + 1 plantilla Excel, y descarga el Excel final con todas las pestañas llenas.")

# ---- Sidebar: instrucciones (UX claro)
with st.sidebar:
    st.header("Checklist de carga")
    st.write("Sube los archivos correctos en cada campo. El sistema valida y arma el Excel final.")
    st.markdown("- ✅ 1) Manejantes (CSV)\n- ✅ 2) Presencias (CSV)\n- ✅ 3) SOVI (CSV)\n- ✅ 4) EDF/Cooler Invaded (CSV)\n- ✅ 5) Secos (CSV)\n- ✅ 6) Plantilla (XLSX)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Carga de archivos")
    manejantes = st.file_uploader("1) Manejantes (CSV)", type=["csv"])
    presencias = st.file_uploader("2) Presencias (CSV)", type=["csv"])
    sovi = st.file_uploader("3) SOVI (CSV)", type=["csv"])
    edf = st.file_uploader("4) EDF / Cooler Invaded (CSV)", type=["csv"])
    secos = st.file_uploader("5) Secos (CSV)", type=["csv"])
    plantilla = st.file_uploader("6) Plantilla Excel (XLSX)", type=["xlsx"])

with col2:
    st.subheader("🧾 Estado")
    ready = all([manejantes, presencias, sovi, edf, secos, plantilla])
    st.metric("Archivos cargados", 6 if ready else sum(x is not None for x in [manejantes,presencias,sovi,edf,secos,plantilla]), 0)
    st.info("Cuando estén los 6 archivos, podrás generar el Excel.")

st.divider()

# ---- Acción principal
if ready:
    st.success("✅ Todo listo. Genera el Excel final.")
    if st.button("🚀 Generar Excel", use_container_width=True):
        try:
            with st.spinner("Procesando..."):
                output_bytes = build_workbook_bytes(
                    template_xlsx_file=plantilla,
                    manejantes_csv=manejantes,
                    presencias_csv=presencias,
                    sovi_csv=sovi,
                    edf_csv=edf,
                    secos_csv=secos,
                )

            st.download_button(
                label="⬇️ Descargar Excel final",
                data=output_bytes,
                file_name="Avance_semanal_Embol_OUTPUT_FINAL.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
            st.balloons()
        except Exception as e:
            st.error("❌ Error al generar el Excel. Revisa que subiste los archivos correctos.")
            st.exception(e)
else:
    st.warning("Carga los 6 archivos para habilitar la generación.")
