import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(layout="wide", page_title="Dashboard Financiero con IA")
st.markdown("<h1 style='text-align: center;'>📊 Dashboard Financiero con IA - Comparación de Empresas</h1>", unsafe_allow_html=True)

# CSS personalizado para modo oscuro
st.markdown("""
    <style>
    body {
        background-color: #111111;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #333333;
        color: white;
    }
    .stDataFrame {
        background-color: #222222;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Entrada de tickers
tickers_input = st.text_input("🧾 Escribí los tickers separados por coma:", value="AAPL,MSFT,GOOGL")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Variables de mercado
rf = 0.04  # Tasa libre de riesgo
rm = 0.09  # Retorno del mercado
kd = 0.06  # Costo de la deuda
tc = 0.25  # Tasa impositiva

resultados = []

for ticker in tickers:
    try:
        empresa = yf.Ticker(ticker)
        info = empresa.info

        nombre = info.get("longName", ticker)
        sector = info.get("sector", "Desconocido")
        industria = info.get("industry", "Desconocida")
        precio = info.get("currentPrice", None)
        deuda = info.get("totalDebt", 0)
        capital = info.get("marketCap", 0)
        ebit = info.get("ebit", 0)
        impuestos = info.get("incomeTaxExpense", 0)
        activos_totales = info.get("totalAssets", 0)
        pasivos_totales = info.get("totalLiab", 0)

        if precio is None:
            continue

        ke = rf + (rm - rf) * info.get("beta", 1)
        e = capital
        d = deuda
        v = e + d
        wacc = ((e/v)*ke) + ((d/v)*kd)*(1 - tc)
        roic = (ebit - impuestos) / (activos_totales - pasivos_totales) if (activos_totales - pasivos_totales) != 0 else 0
        eva = (roic - wacc) * (activos_totales - pasivos_totales)

        genera_valor = "✅ Sí" if eva > 0 else "❌ No"

        resultados.append({
            "Ticker": ticker,
            "Nombre": nombre,
            "Sector": sector,
            "Industria": industria,
            "Precio": precio,
            "ROIC": round(roic * 100, 2),
            "WACC": round(wacc * 100, 2),
            "EVA": round(eva, 2),
            "Genera Valor": genera_valor
        })

    except Exception as e:
        st.warning(f"Error procesando {ticker}: {e}")

# Mostrar resultados
if resultados:
    df_resultados = pd.DataFrame(resultados)
    st.dataframe(df_resultados)

    fig = px.scatter(
        df_resultados,
        x="WACC",
        y="ROIC",
        size="Precio",
        color="Genera Valor",
        hover_name="Nombre",
        title="Comparación ROIC vs WACC"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Por favor, ingresa tickers válidos para analizar.")
  Creación del dashboard financiero
