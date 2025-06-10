import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, kruskal, chi2_contingency, shapiro

# Título de la app
st.title("Hábitos Estudiantiles y Rendimiento Académico")
st.subheader("Análisis basado en datos de 1,000 estudiantes")

# Descripción general
st.write("Este estudio analiza cómo los hábitos de estudio, sueño, trabajo a medio tiempo y asistencia influyen en el rendimiento académico.")
st.write("**Integrantes:** Andres Solorzano, Ismael Vanegas")

# Cargar y limpiar datos
df = pd.read_csv("student_habits_performance.csv")
df = df[["study_hours_per_day", "sleep_hours", "exam_score", "part_time_job", "attendance_percentage"]]
df = df.dropna().drop_duplicates()
df = df.rename(columns={
    "study_hours_per_day": "Horas de Estudio",
    "sleep_hours": "Horas de Sueño",
    "exam_score": "Nota del Examen",
    "part_time_job": "Trabajo Medio Tiempo",
    "attendance_percentage": "Porcentaje de Asistencia"})

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

# Prueba de normalidad por grupo
trabajo_si = df[df["Trabajo Medio Tiempo"] == "Yes"]["Nota del Examen"]
trabajo_no = df[df["Trabajo Medio Tiempo"] == "No"]["Nota del Examen"]

dos_uno=st.toggle("2.1 Prueba de normalidad por grupo de trabajo")
if dos_uno:
    st.subheader("2.1 Prueba de normalidad por grupo de trabajo")

    
    # Prueba de Shapiro-Wilk
    stat_si, p_si = shapiro(trabajo_si)
    stat_no, p_no = shapiro(trabajo_no)

    st.write("**Resultados de la prueba de normalidad (Shapiro-Wilk):**")
    st.write(f"Estudiantes CON trabajo - Valor P: {p_si:.4f}")
    st.write(f"Estudiantes SIN trabajo - Valor P: {p_no:.4f}")

    st.markdown("**Conclusión 2.1:** Ninguno de los grupos presenta una distribución normal (p < 0.05), por lo tanto se usará una prueba no paramétrica (Kruskal-Wallis).")


# Prueba de Kruskal-Wallis
dos_dos=st.toggle("2.2 Comparación de notas con prueba de Kruskal-Wallis")
if dos_dos:
    st.subheader("2.2 Comparación de notas con prueba de Kruskal-Wallis")

    fig_k = px.box(df, x="Trabajo Medio Tiempo", y="Nota del Examen", color="Trabajo Medio Tiempo",
                title="Trabajo Medio Tiempo vs Nota del Examen")
    st.plotly_chart(fig_k)

    stat_k, p_k = kruskal(trabajo_si, trabajo_no)

    st.write("**Prueba de Kruskal-Wallis:**")
    st.write(f"Estadístico: {stat_k:.3f}, Valor P: {p_k:.4f}")

    st.markdown("**Conclusión 2.2:** Se compararon las notas entre estudiantes con y sin trabajo. No se encontró diferencia estadísticamente significativa (p ≥ 0.05), por lo tanto no se puede afirmar que el trabajo influya directamente en las notas.")

# Relación visual entre asistencia y nota por tipo de trabajo
dos_tres=st.toggle("2.3 Relación visual entre Asistencia y Nota del Examen por tipo de Trabajo")
if dos_tres:
    st.subheader("2.3 Relación visual entre Asistencia y Nota del Examen por tipo de Trabajo")

    fig_asistencia = px.scatter(df, x="Porcentaje de Asistencia", y="Nota del Examen", color="Trabajo Medio Tiempo",
                                title="Asistencia vs Nota del Examen por tipo de Trabajo")
    st.plotly_chart(fig_asistencia)

    st.markdown("**Conclusión 2.3:** El gráfico permite observar que una alta asistencia podría relacionarse con mejor rendimiento, incluso en quienes trabajan.")

# Prueba de Chi-cuadrado: Trabajo vs Rendimiento (Alto/Bajo)
dos_cuatro=st.toggle("2.4 Relación entre Trabajo y Nivel de Rendimiento (Chi-cuadrado)")
if dos_cuatro:
    st.subheader("2.4 Relación entre Trabajo y Nivel de Rendimiento (Chi-cuadrado)")

    # Crear variable categórica rendimiento
    df["Rendimiento"] = pd.cut(df["Nota del Examen"], bins=[0, 69.99, 100], labels=["Bajo", "Alto"])

    # Tabla de contingencia
    tabla = pd.crosstab(df["Trabajo Medio Tiempo"], df["Rendimiento"])
    st.write("**Tabla de contingencia:**")
    st.dataframe(tabla)

    # Prueba de chi-cuadrado
    chi2, p_chi, dof, expected = chi2_contingency(tabla)

    st.write("**Prueba de Chi-cuadrado:**")
    st.write(f"Estadístico: {chi2:.3f}, Valor P: {p_chi:.4f}")

    st.markdown("**Conclusión 2.4:** La prueba evalúa si existe relación entre tener trabajo y el nivel de rendimiento académico. No se observó una relación significativa (p ≥ 0.05), por lo que no se puede afirmar que el trabajo esté asociado con un nivel específico de rendimiento.")
    
