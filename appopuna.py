import streamlit as st
import sympy as sp
import pandas as pd

# Configuración de la página web
st.set_page_config(page_title="Optimización de Una Variable", page_icon="📈", layout="wide")

st.title("📈 Laboratorio de Optimización de Una Variable (Sin Restricciones)")
st.markdown("Análisis interactivo paso a paso mediante el **Criterio de la Segunda Derivada**.")

# =========================================================================
# BARRA LATERAL: INGRESO DE DATOS
# =========================================================================
st.sidebar.header("📥 Configuración de la Función")

# Ejemplo sugerido adaptado para que coincida con la estructura limpia de exponenciales
funcion_str = st.sidebar.text_input("Función Objetivo f(x):", value="x * exp(3*x)")
variable_str = st.sidebar.text_input("Variable de estudio:", value="x")

st.sidebar.info("**Criterio de la Segunda Derivada Activo:**\n"
                "Sea $c$ un valor crítico obtenido de $f'(x) = 0$:\n"
                "• Si $f''(c) > 0 \\implies$ Mínimo en $(c, f(c))$\n"
                "• Si $f''(c) < 0 \\implies$ Máximo en $(c, f(c))$\n"
                "• Si $f''(c) = 0 \\implies$ Punto Silla en $(c, f(c))$")

calcular = st.sidebar.button("Calcular Optimización", type="primary")

# =========================================================================
# MOTOR DE CÁLCULO ALGEBRAICO
# =========================================================================
if calcular:
    try:
        # Configurar variable y función
        var = sp.Symbol(variable_str.strip())
        
        # Reemplazar posibles variantes de 'e' por la función exponencial nativa de SymPy
        raw_func = funcion_str.replace("e**", "exp").replace("e^", "exp")
        f = sp.sympify(raw_func)

        # 1. Cálculo de derivadas y simplificación estricta (asumiendo log(e) = 1)
        # Factorizamos para que los alumnos vean la estructura matemática ideal
        primera_der = sp.factor(sp.simplify(sp.diff(f, var)))  
        segunda_der = sp.factor(sp.simplify(sp.diff(primera_der, var))) 

        st.header("1. Modelado Analítico y Derivadas")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Función Original:**")
            st.latex(rf"f({sp.latex(var)}) = {sp.latex(f)}")
        with col2:
            st.markdown("**Primera Derivada (Factorizada):**")
            st.latex(rf"f'({sp.latex(var)}) = {sp.latex(primera_der)}")
        with col3:
            st.markdown("**Segunda Derivada (Factorizada):**")
            st.latex(rf"f''({sp.latex(var)}) = {sp.latex(segunda_der)}")

        st.divider()

        # 2. Obtención de Puntos Críticos f'(x) = 0
        st.header("2. Determination de Puntos Críticos")
        st.markdown(rf"Igualamos la primera derivada a cero para hallar los valores críticos de la función:")
        st.latex(rf"f'({sp.latex(var)}) = {sp.latex(primera_der)} = 0")

        # Resolver en el campo de los números reales
        soluciones = sp.solve(sp.Eq(primera_der, 0), var)
        pc = sorted([sol for sol in soluciones if sol.is_real])

        if not pc:
            st.warning("No se encontraron puntos críticos reales para esta función. (Ej. Exponenciales puras que nunca tocan cero).")
        else:
            npc = len(pc)
            st.success(f"Se han detectado {npc} valor(es) crítico(s) real(es):")
            
            puntos_criticos_latex = ", ".join([f"c_{{idx+1}} = {sp.latex(c)}" for idx, c in enumerate(pc)])
            st.latex(rf"\left\{{ {puntos_criticos_latex} \right\}}")

            st.divider()

            # 3. Clasificación usando estrictamente la Segunda Derivada
            st.header("3. Clasificación de Extremos (Criterio de la Segunda Derivada)")
            st.markdown(rf"Evaluamos cada valor crítico $c$ en la segunda derivada $f''(c)$ para dictaminar su naturaleza:")

            datos_puntos = []
            for i, c in enumerate(pc):
                val_c = float(c.evalf())
                val_f = float(f.subs(var, c).evalf())
                val_sd = float(segunda_der.subs(var, c).evalf())
                
                # Clasificación analítica según las tres condiciones requeridas
                if val_sd > 0:
                    tipo_extremo = "🟢 Mínimo"
                    condicion_latex = rf"f''({val_c:.3f}) = {val_sd:.3f} > 0"
                elif val_sd < 0:
                    tipo_extremo = "🔵 Máximo"
                    condicion_latex = rf"f''({val_c:.3f}) = {val_sd:.3f} < 0"
                else:
                    tipo_extremo = "🟡 Punto Silla"
                    condicion_latex = rf"f''({val_c:.3f}) = 0"
                
                datos_puntos.append({
                    "Punto Crítico": f"c_{i+1} = {val_c:.3f}",
                    "Condición": f"$ {condicion_latex} $",
                    "Coordenada (c, f(c))": f"({val_c:.3f}, {val_f:.3f})",
                    "Resultado Analítico": tipo_extremo
                })

            # Mostrar tabla final limpia
            df_resultado = pd.DataFrame(datos_puntos)
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error en el cálculo: {e}. Revisa la expresión matemática ingresada.")
