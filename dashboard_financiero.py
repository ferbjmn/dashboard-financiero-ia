import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configuración general
st.set_page_config(page_title="Dashboard Financiero Estilo DeepSeek", layout="wide")

# Estética DeepSeek V3
st.markdown("""
    <style>
    body { background-color: #0d1117; color: #c9d1d9; }
    .stApp { background-color: #0d1117; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3, h4, .markdown-text-container { color: #58a6ff; }
    .metric-container { padding: 1rem; border-radius: 12px; background-color: #161b22; margin-bottom: 10px; }
    .metric-label { font-size: 0.8rem; color: #8b949e; }
    .metric-value { font-size: 1.3rem; font-weight: bold; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align: center;'>📊 Dashboard Financiero - Estética DeepSeek V3</h1>", unsafe_allow_html=True)

# Input de Tickers
tickers_input = st.text_input("🧾 Escribí los tickers separados por coma:", value="AAPL,MSFT,GOOGL")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Variables financieras
rf, rm, kd, tc = 0.04, 0.09, 0.06, 0.25
resultados = []

for ticker in tickers:
    try:
        empresa = yf.Ticker(ticker)
        info = empresa.info

        nombre = info.get("longName", ticker)
        sector = info.get("sector", "Desconocido")
        industria = info.get("industry", "Desconocida")
        precio = info.get("currentPrice", 0)
        deuda = info.get("totalDebt", 0)
        capital = info.get("marketCap", 0)
        ebit = info.get("ebit", 0)
        impuestos = info.get("incomeTaxExpense", 0)
        activos_totales = info.get("totalAssets", 0)
        pasivos_totales = info.get("totalLiab", 0)
        logo = info.get("logo_url", "")

        pe = info.get("trailingPE", 0)
        pb = info.get("priceToBook", 0)
        pfcf = info.get("priceToFreeCashFlows", 0)
        dividend_years = info.get("dividendRate", 0)
        dividend_yield = info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0
        payout_ratio = info.get("payoutRatio", 0) * 100 if info.get("payoutRatio") else 0
        roa = info.get("returnOnAssets", 0) * 100 if info.get("returnOnAssets") else 0
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
        current_ratio = info.get("currentRatio", 0)
        lt_debt_eq = info.get("longTermDebtEquity", 0)
        debt_eq = info.get("debtToEquity", 0)
        op_margin = info.get("operatingMargins", 0) * 100 if info.get("operatingMargins") else 0
        profit_margin = info.get("profitMargins", 0) * 100 if info.get("profitMargins") else 0

        ke = rf + (rm - rf) * info.get("beta", 1)
        e, d = capital, deuda
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
            "P/E": round(pe, 2),
            "P/B": round(pb, 2),
            "P/FCF": round(pfcf, 2),
            "Dividend Years": dividend_years,
            "Dividend Yield %": round(dividend_yield, 2),
            "Payout Ratio": round(payout_ratio, 2),
            "ROA": round(roa, 2),
            "ROE": round(roe, 2),
            "Current Ratio": round(current_ratio, 2),
            "LT Debt/Equity": round(lt_debt_eq, 2),
            "Debt/Equity": round(debt_eq, 2),
            "Operating Margin": round(op_margin, 2),
            "Profit Margin": round(profit_margin, 2),
            "Genera Valor": genera_valor,
            "Logo": logo
        })

    except Exception as e:
        st.warning(f"Error procesando {ticker}: {e}")

# Mostrar
if resultados:
    df = pd.DataFrame(resultados)

    for row in df.itertuples():
        st.markdown("---")
        col1, col2 = st.columns([1, 6])
        with col1:
            if row.Logo:
                st.image(row.Logo, width=60)
        with col2:
            st.markdown(f"### {row.Nombre}")
            st.markdown(f"**Sector:** {row.Sector}  \n**Industria:** {row.Industria}")

            metrics = [
                ("💰 Precio", row.Precio),
                ("📊 ROIC", f"{row.ROIC}%"),
                ("💼 WACC", f"{row.WACC}%"),
                ("📈 EVA", row.EVA),
                ("🧮 P/E", row._9),
                ("📘 P/B", row._10),
                ("💵 P/FCF", row._11),
                ("📅 Div Years", row._12),
                ("💹 Div Yield %", f"{row._13}%"),
                ("🔁 Payout Ratio", f"{row._14}%"),
                ("📈 ROA", f"{row._15}%"),
                ("📈 ROE", f"{row._16}%"),
                ("💧 Current Ratio", row._17),
                ("🏦 LT Debt/Eq", row._18),
                ("🏦 Debt/Eq", row._19),
                ("📉 Op Margin", f"{row._20}%"),
                ("📉 Profit Margin", f"{row._21}%")
            ]

            rows = [metrics[i:i+6] for i in range(0, len(metrics), 6)]
            for fila in rows:
                cols = st.columns(len(fila))
                for (label, val), col in zip(fila, cols):
                    col.markdown(f"<div class='metric-container'><div class='metric-label'>{label}</div><div class='metric-value'>{val}</div></div>", unsafe_allow_html=True)

    fig = px.scatter(
        df, x="WACC", y="ROIC", color="Genera Valor", size="Precio",
        hover_name="Nombre", title="Comparación ROIC vs WACC", template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Tabla comparativa")
    st.dataframe(df.drop("Logo", axis=1), use_container_width=True)
else:
    st.info("📌 Ingresá tickers válidos para comenzar el análisis.")
