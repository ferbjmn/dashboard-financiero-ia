import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Financiero Estilo DeepSeek", layout="wide")

# Estética DeepSeek V3
st.markdown("""
<style>
body { background-color: #0d1117; color: #c9d1d9; }
.stApp { background-color: #0d1117; font-family: 'Segoe UI', sans-serif; }
h1, h2, h3, .markdown-text-container { color: #58a6ff; }
.metric-box {
    padding: 0.5rem;
    margin: 0.3rem;
    border-radius: 10px;
    background-color: #161b22;
    text-align: center;
}
.metric-label { font-size: 0.75rem; color: #8b949e; }
.metric-value { font-size: 1.2rem; font-weight: bold; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📊 Dashboard Financiero - Estética DeepSeek V3</h1>", unsafe_allow_html=True)

tickers_input = st.text_input("🧾 Escribí los tickers separados por coma:", value="AAPL,MSFT,GOOGL")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

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
        activos = info.get("totalAssets", 0)
        pasivos = info.get("totalLiab", 0)

        pe = info.get("trailingPE", 0)
        pb = info.get("priceToBook", 0)
        pfcf = info.get("priceToFreeCashFlows", 0)
        dividend_years = info.get("dividendRate", 0)
        dividend_yield = (info.get("dividendYield", 0) or 0) * 100
        payout_ratio = (info.get("payoutRatio", 0) or 0) * 100
        roa = (info.get("returnOnAssets", 0) or 0) * 100
        roe = (info.get("returnOnEquity", 0) or 0) * 100
        current_ratio = info.get("currentRatio", 0)
        lt_debt_eq = info.get("longTermDebtEquity", 0)
        debt_eq = info.get("debtToEquity", 0)
        op_margin = (info.get("operatingMargins", 0) or 0) * 100
        profit_margin = (info.get("profitMargins", 0) or 0) * 100

        ke = rf + (rm - rf) * info.get("beta", 1)
        e, d = capital, deuda
        v = e + d
        wacc = ((e/v)*ke + (d/v)*kd*(1 - tc)) if v != 0 else 0
        capital_invertido = activos - pasivos
        roic = ((ebit - impuestos) / capital_invertido) if capital_invertido != 0 else 0
        eva = (roic - wacc) * capital_invertido if capital_invertido != 0 else 0
        genera_valor = "✅ Sí" if eva > 0 else "❌ No"

        resultados.append({
            "Ticker": ticker,
            "Nombre": nombre,
            "Sector": sector,
            "Industria": industria,
            "Precio": precio,
            "ROIC": roic * 100,
            "WACC": wacc * 100,
            "EVA": eva,
            "P/E": pe,
            "P/B": pb,
            "P/FCF": pfcf,
            "Dividend Years": dividend_years,
            "Dividend Yield %": dividend_yield,
            "Payout Ratio": payout_ratio,
            "ROA": roa,
            "ROE": roe,
            "Current Ratio": current_ratio,
            "LT Debt/Equity": lt_debt_eq,
            "Debt/Equity": debt_eq,
            "Operating Margin": op_margin,
            "Profit Margin": profit_margin,
            "Genera Valor": genera_valor,
        })

    except Exception as e:
        st.warning(f"Error procesando {ticker}: {e}")

if resultados:
    df = pd.DataFrame(resultados)

    for row in df.itertuples():
        st.markdown(f"### {row.Nombre}")
        st.markdown(f"**Sector:** {row.Sector}  \n**Industria:** {row.Industria}")
        datos = [
            ("💰 Precio", row.Precio),
            ("📊 ROIC", f"{row.ROIC:.2f}%"),
            ("📦 WACC", f"{row.WACC:.2f}%"),
            ("📈 EVA", f"{row.EVA:,.2f}"),
            ("🧮 P/E", row._9),
            ("📘 P/B", row._10),
            ("💵 P/FCF", row._11),
            ("📅 Div Years", row._12),
            ("💹 Div Yield %", f"{row._13:.2f}%"),
            ("🔁 Payout Ratio", f"{row._14:.2f}%"),
            ("📈 ROA", f"{row._15:.2f}%"),
            ("📈 ROE", f"{row._16:.2f}%"),
            ("💧 Current Ratio", row._17),
            ("🏦 LT Debt/Eq", row._18),
            ("🏦 Debt/Eq", row._19),
            ("📉 Op Margin", f"{row._20:.2f}%"),
            ("📉 Profit Margin", f"{row._21:.2f}%")
        ]
        filas = [datos[i:i+6] for i in range(0, len(datos), 6)]
        for fila in filas:
            cols = st.columns(len(fila))
            for (label, val), col in zip(fila, cols):
                col.markdown(f"<div class='metric-box'><div class='metric-label'>{label}</div><div class='metric-value'>{val}</div></div>", unsafe_allow_html=True)
        st.markdown("---")

    # Gráfico comparativo tipo GuruFocus
    st.subheader("📊 Comparación ROIC vs WACC (Estilo GuruFocus)")
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df["Nombre"],
        x=df["WACC"],
        name="WACC",
        orientation='h',
        marker_color='orange'
    ))

    fig.add_trace(go.Bar(
        y=df["Nombre"],
        x=df["ROIC"],
        name="ROIC",
        orientation='h',
        marker_color='lightgreen'
    ))

    fig.update_layout(
        barmode='group',
        xaxis_title="Porcentaje",
        yaxis_title="Empresa",
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tabla comparativa
    st.markdown("### 📋 Tabla comparativa")
    st.dataframe(df.drop(columns=["Genera Valor"]), use_container_width=True)

else:
    st.info("📌 Ingresá tickers válidos para ver la comparación.")
