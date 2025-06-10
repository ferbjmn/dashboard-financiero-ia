import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Financiero Bloomberg Style", layout="wide")

# Estilo oscuro profesional
st.markdown("""
    <style>
    body {background-color: #0d1117; color: #c9d1d9;}
    .stApp {background-color: #0d1117;}
    h1, h2, h3, h4 {color: #58a6ff;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📈 Dashboard Financiero - Estilo Bloomberg</h1>", unsafe_allow_html=True)

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

if resultados:
    df = pd.DataFrame(resultados)

    for i, row in df.iterrows():
        with st.container():
            st.markdown("---")
            cols = st.columns([1, 3, 2, 2, 2, 2])
            with cols[0]:
                if row["Logo"]:
                    st.image(row["Logo"], width=60)
            with cols[1]:
                st.markdown(f"### {row['Nombre']}")
                st.markdown(f"**Sector:** {row['Sector']}  \n**Industria:** {row['Industria']}")
            with cols[2]:
                st.metric("💰 Precio", f"${row['Precio']}")
                st.metric("📊 ROIC", f"{row['ROIC']}%")
                st.metric("💼 WACC", f"{row['WACC']}%")
                st.metric("📈 EVA", f"{row['EVA']}")
                st.metric("🎯 Genera Valor", row["Genera Valor"])
            with cols[3]:
                st.metric("🧮 P/E", row["P/E"])
                st.metric("📘 P/B", row["P/B"])
                st.metric("💵 P/FCF", row["P/FCF"])
                st.metric("📅 Div Years", row["Dividend Years"])
            with cols[4]:
                st.metric("💹 Div Yield %", f"{row['Dividend Yield %']}%")
                st.metric("🔁 Payout Ratio", f"{row['Payout Ratio']}%")
                st.metric("📈 ROA", f"{row['ROA']}%")
                st.metric("📈 ROE", f"{row['ROE']}%")
            with cols[5]:
                st.metric("💧 Current Ratio", row["Current Ratio"])
                st.metric("🏦 LT Debt/Eq", row["LT Debt/Equity"])
                st.metric("🏦 Debt/Eq", row["Debt/Equity"])
                st.metric("📉 Op Margin", f"{row['Operating Margin']}%")
                st.metric("📉 Profit Margin", f"{row['Profit Margin']}%")

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

    # Tabla completa
    st.markdown("### 📋 Tabla comparativa completa")
    st.dataframe(df.drop("Logo", axis=1), use_container_width=True)

else:
    st.info("📌 Ingresá tickers válidos para comenzar el análisis.")
