import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configuración general del layout
st.set_page_config(page_title="Dashboard Financiero Bloomberg Style", layout="wide")

# Estilo visual tipo Bloomberg
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stApp {
        background-color: #0d1117;
    }
    h1, h2, h3, h4 {
        color: #58a6ff;
    }
    .metric-label {
        font-weight: bold;
        color: #8b949e;
    }
    .metric-value {
        font-size: 24px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center;'>📈 Dashboard Financiero - Estilo Bloomberg</h1>", unsafe_allow_html=True)

# Entrada de tickers
tickers_input = st.text_input("🧾 Escribí los tickers separados por coma:", value="AAPL,MSFT,GOOGL")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Variables del modelo
rf = 0.04
rm = 0.09
kd = 0.06
tc = 0.25

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
        logo = info.get("logo_url", "")

        if precio is None:
            continue

        ke = rf + (rm - rf) * info.get("beta", 1)
        e = capital
        d = deuda
        v = e + d
        wacc = ((e/v)*ke) + ((d/v)*kd)*(1 - tc)
        capital_invertido = activos_totales - pasivos_totales
        roic = (ebit - impuestos) / capital_invertido if capital_invertido != 0 else 0
        eva = (roic - wacc) * capital_invertido
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
            "Genera Valor": genera_valor,
            "Logo": logo
        })

    except Exception as e:
        st.warning(f"Error al procesar {ticker}: {e}")

# Mostrar resultados
if resultados:
    df = pd.DataFrame(resultados)

    for i, row in df.iterrows():
        with st.container():
            cols = st.columns([1, 2, 2, 2, 2])
            with cols[0]:
                if row["Logo"]:
                    st.image(row["Logo"], width=60)
            with cols[1]:
                st.markdown(f"### {row['Nombre']}")
                st.markdown(f"**Sector:** {row['Sector']}  \n**Industria:** {row['Industria']}")
            with cols[2]:
                st.metric("💰 Precio", f"${row['Precio']}")
            with cols[3]:
                st.metric("📊 ROIC", f"{row['ROIC']}%")
                st.metric("💼 WACC", f"{row['WACC']}%")
            with cols[4]:
                st.metric("📈 EVA", f"{row['EVA']}")
                st.metric("🎯 Genera Valor", row["Genera Valor"])
            st.markdown("---")

    # Gráfico
    fig = px.scatter(
        df,
        x="WACC",
        y="ROIC",
        color="Genera Valor",
        size="Precio",
        hover_name="Nombre",
        title="Comparación ROIC vs WACC",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabla
    st.markdown("### 📋 Tabla comparativa")
    st.dataframe(df.drop("Logo", axis=1), use_container_width=True)

else:
    st.info("📌 Por favor, ingresá tickers válidos para comenzar el análisis.")
