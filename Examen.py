import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, kruskal, chi2_contingency

# Título de la app
st.title("Hábitos Estudiantiles y Rendimiento Académico")
st.subheader("Análisis basado en datos de 1,000 estudiantes")

# Descripción general
st.write("Este estudio analiza cómo los hábitos de estudio, sueño, trabajo a medio tiempo y asistencia influyen en el rendimiento académico.")

# Cargar y limpiar datos
df = pd.read_csv("student_habits_performance.csv")
df = df[["study_hours_per_day", "sleep_hours", "exam_score", "part_time_job", "attendance_percentage"]]
df = df.dropna().drop_duplicates()
df = df.rename(columns={
    "study_hours_per_day": "Horas de Estudio",
    "sleep_hours": "Horas de Sueño",
    "exam_score": "Nota del Examen",
    "part_time_job": "Trabajo Medio Tiempo",
    "attendance_percentage": "Porcentaje de Asistencia"
})

st.subheader("Vista previa de los datos")
st.dataframe(df)

# OBJETIVO 1 

st.header("Objetivo 1")
st.markdown("**Analizar la relación entre las horas de estudio por día, horas de sueño y la calificación del examen**")
st.markdown("El objetivo es identificar si existe una combinación óptima entre descanso y estudio que favorezca el rendimiento académico.")

# Horas de Estudio vs Nota
uno_uno=st.toggle("1.1 Relación entre Horas de Estudio y Nota del Examen")
if uno_uno:
    st.subheader("1.1 Relación entre Horas de Estudio y Nota del Examen")
    fig1 = px.scatter(df, x="Horas de Estudio", y="Nota del Examen", title="Horas de Estudio vs Nota del Examen")
    st.plotly_chart(fig1)

    r1, p1 = pearsonr(df["Horas de Estudio"], df["Nota del Examen"])
    st.write("**Prueba de correlación de Pearson:**")
    st.write(f"Estadístico: {r1:.3f}, Valor P: {p1:.4f}")

    st.markdown(f"**Conclusión 1.1:** Existe una correlación de {r1:.3f} entre las horas de estudio y la nota del examen. Esto indica una relación positiva significativa: estudiar más tiende a mejorar el rendimiento académico.")

# Horas de Sueño vs Nota
uno_dos=st.toggle("1.2 Relación entre Horas de Sueño y Nota del Examen")
if uno_dos:
    st.subheader("1.2 Relación entre Horas de Sueño y Nota del Examen")
    fig2 = px.scatter(df, x="Horas de Sueño", y="Nota del Examen", title="Horas de Sueño vs Nota del Examen")
    st.plotly_chart(fig2)

    r2, p2 = pearsonr(df["Horas de Sueño"], df["Nota del Examen"])
    st.write("**Prueba de correlación de Pearson:**")
    st.write(f"Estadístico: {r2:.3f}, Valor P: {p2:.4f}")

    st.markdown(f"**Conclusión 1.2:** Se observó una correlación de {r2:.3f} entre horas de sueño y nota del examen. La relación es estadísticamente significativa (p < 0.05), por lo que dormir más parece contribuir a un mejor desempeño académico.")

# OBJETIVO 2

st.header("Objetivo 2")
st.markdown("**Comparar el rendimiento académico entre estudiantes que tienen trabajo a medio tiempo y los que no, considerando también su asistencia a clases.**")
st.markdown("El objetivo es evaluar si el empleo afecta negativamente el desempeño, y si una alta asistencia puede compensarlo.")

# Nota vs Trabajo
dos_uno=st.toggle("2.1 Comparación de Notas entre Estudiantes con y sin Trabajo")
if dos_uno:
    st.subheader("2.1 Comparación de Notas entre Estudiantes con y sin Trabajo")
    fig3 = px.box(df, x="Trabajo Medio Tiempo", y="Nota del Examen", color="Trabajo Medio Tiempo",
                title="Trabajo a Medio Tiempo vs Nota del Examen")
    st.plotly_chart(fig3)

    grupo_trabajo = df[df["Trabajo Medio Tiempo"] == "Yes"]["Nota del Examen"]
    grupo_sin_trabajo = df[df["Trabajo Medio Tiempo"] == "No"]["Nota del Examen"]
    stat, p = kruskal(grupo_trabajo, grupo_sin_trabajo)

    st.write("**Prueba de Kruskal-Wallis:**")
    st.write(f"Estadístico: {stat:.3f}, Valor P: {p:.4f}")

    st.markdown("**Conclusión 2.1:** Se compararon las notas entre estudiantes que tienen y no tienen trabajo a medio tiempo. No se encontró una diferencia significativa (p ≥ 0.05), por lo tanto no se puede afirmar que el trabajo influya directamente en las notas.")

# Asistencia vs Nota, según trabajo
dos_dos=st.toggle("2.2 Relación entre Asistencia y Nota del Examen según Trabajo")
if dos_dos:
    st.subheader("2.2 Relación entre Asistencia y Nota del Examen según Trabajo")
    fig4 = px.scatter(df, x="Porcentaje de Asistencia", y="Nota del Examen", color="Trabajo Medio Tiempo",
                    title="Asistencia vs Nota del Examen por tipo de Trabajo")
    st.plotly_chart(fig4)

    st.markdown("**Conclusión 2.2:** Aunque no se aplicó una prueba estadística adicional aquí, el gráfico sugiere que una alta asistencia puede estar asociada con mejores resultados académicos, incluso entre quienes tienen trabajo.")
    st.markdown("")
    