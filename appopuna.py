import streamlit as st
import sympy as sp
import pandas as pd

# Configuración de la página web
st.set_page_config(page_title="Optimización de Una Variable", page_icon="📈", layout="wide")

st.title("📈 Laboratorio de Optimización de Una Variable (Sin Restricciones)")
st.markdown("Análisis interactivo paso a paso: Criterio de la Primera y Segunda Derivada.")

# =========================================================================
# BARRA LATERAL: INGRESO DE DATOS
# =========================================================================
st.sidebar.header("📥 Configuración de la Función")

funcion_str = st.sidebar.text_input("Función Objetivo f(x):", value="x**3 - 3*x**2 - 9*x + 5")
variable_str = st.sidebar.text_input("Variable de estudio:", value="x")

st.sidebar.info("**Criterios de Optimización:**\n"
                "• Puntos Críticos: $f'(x) = 0$\n"
                "• Si $f''(x_c) < 0 \\implies$ Máximo local.\n"
                "• Si $f''(x_c) > 0 \\implies$ Mínimo local.\n"
                "• Entornos $\\pm 0.1$ para evaluar crecimiento.")

calcular = st.sidebar.button("Calcular Optimización Libre", type="primary")

# =========================================================================
# MOTOR DE CÁLCULO ALGEBRAICO (UNA VARIABLE)
# =========================================================================
if calcular:
    try:
        # Configurar variable y función
        var = sp.Symbol(variable_str.strip())
        f = sp.sympify(funcion_str)

        # 1. Cálculo de derivadas
        pd = sp.diff(f, var)  # Primera derivada
        sd = sp.diff(pd, var) # Segunda derivada

        st.header("1. Modelado Analítico y Derivadas")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Función Original:**")
            st.latex(rf"f({sp.latex(var)}) = {sp.latex(f)}")
        with col2:
            st.markdown("**Primera Derivada (Pendiente):**")
            st.latex(rf"f'({sp.latex(var)}) = {sp.latex(pd)}")
        with col3:
            st.markdown("**Segunda Derivada (Concavidad):**")
            st.latex(rf"f''({sp.latex(var)}) = {sp.latex(sd)}")

        st.divider()

        # 2. Obtención de Puntos Críticos (Reals)
        st.header("2. Determinación de Puntos Críticos")
        st.markdown(rf"Resolvemos la ecuación fundamental $f'({sp.latex(var)}) = 0$ para hallar los valores críticos:")
        st.latex(rf"{sp.latex(pd)} = 0")

        # Resolver numéricamente y analíticamente en el campo real
        soluciones = sp.solve(sp.Eq(pd, 0), var)
        pc = sorted([sol for sol in soluciones if sol.is_real])

        if not pc:
            st.warning("No se encontraron puntos críticos reales para esta función. No presenta máximos ni mínimos libres.")
        else:
            npc = len(pc)
            st.success(f"Se han detectado {npc} punto(s) crítico(s) real(es):")
            
            puntos_criticos_latex = ", ".join([f"{sp.latex(c)}" for c in pc])
            st.latex(rf"{sp.latex(var)}_c \in \left\{{ {puntos_criticos_latex} \right\}}")

            st.divider()

            # 3. Análisis de comportamiento por intervalos (Primera Derivada - 'crece' / 'decrece')
            st.header("3. Criterio de la Primera Derivada (Comportamiento de Intervalos)")
            st.markdown("Evaluamos el signo de la pendiente en entornos inmediatamente anteriores y posteriores a cada valor crítico:")

            # Construir tabla de intervalos simulando la lógica de maxmin2 de Mathematica
            intervalos_lista = []
            
            # Agregar el extremo izquierdo (-infinito) hasta el primer punto crítico
            pc_extendido = [-sp.oo] + pc + [sp.oo]
            
            datos_intervalos = []
            for i in range(len(pc_extendido) - 1):
                inf = pc_extendido[i]
                sup = pc_extendido[i+1]
                
                # Definir etiqueta visual del intervalo abierta
                label_intervalo = f"<{inf}, {sup}>"
                
                # Definir punto de prueba en el entorno (Lógica Mathematica pc - 0.1 o pc + 0.1)
                if inf == -sp.oo:
                    punto_prueba = float(sup) - 0.1
                elif sup == sp.oo:
                    punto_prueba = float(inf) + 0.1
                else:
                    punto_prueba = (float(inf) + float(sup)) / 2.0
                
                # Evaluar signo en la primera derivada
                valor_derivada = float(pd.subs(var, punto_prueba).evalf())
                estado = "📈 Crece" if valor_derivada > 0 else "📉 Decrece"
                
                datos_intervalos.append({
                    "Intervalo Evaluado": label_intervalo,
                    "Punto de Prueba Usado": f"{punto_prueba:.3f}",
                    "Signo f'(x)": f"{valor_derivada:.4f}",
                    "Comportamiento f(x)": estado
                })
            
            st.dataframe(pd.DataFrame(datos_intervalos), use_container_width=True, hide_index=True)

            st.divider()

            # 4. Clasificación mediante la Segunda Derivada
            st.header("4. Criterio de la Segunda Derivada y Clasificación de Extremos")
            st.markdown(rf"Sustituimos cada valor crítico en $f''({sp.latex(var)})$ para determinar el tipo de extremo:")

            datos_puntos = []
            for i, c in enumerate(pc):
                val_c = float(c.evalf())
                val_f = float(f.subs(var, c).evalf())
                val_sd = float(sd.subs(var, c).evalf())
                
                # Clasificación de acuerdo a la concavidad (sd)
                if val_sd < 0:
                    tipo_extremo = "🔵 Máximo Local"
                    explicacion_concavidad = "Concavidad hacia abajo (f'' < 0)"
                elif val_sd > 0:
                    tipo_extremo = "🟢 Mínimo Local"
                    explicacion_concavidad = "Concavidad hacia arriba (f'' > 0)"
                else:
                    tipo_extremo = "🟡 Inflexión / Dudoso"
                    explicacion_concavidad = "Hessiano nulo (f'' = 0)"
                
                datos_puntos.append({
                    "Punto Crítico": f"x_{i+1} = {val_c:.3f}",
                    "Coordenada Exacta (x, f(x))": f"({val_c:.3f}, {val_f:.3f})",
                    "Evaluación f''(x_c)": f"{val_sd:.4f}",
                    "Comportamiento Geométrico": explicacion_concavidad,
                    "Clasificación Final": tipo_extremo
                })

            st.dataframe(pd.DataFrame(datos_puntos), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error general en el cálculo: {e}. Asegúrate de ingresar una función matemática válida.")