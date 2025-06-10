import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Financiero Estilo Claro", layout="wide")

# Estética clara personalizada
st.markdown("""
<style>
body { background-color: white; color: black; }
.stApp { background-color: white; font-family: 'Segoe UI', sans-serif; }
h1, h2, h3, .markdown-text-container { color: #1f4e79; }
.metric-box {
    padding: 0.5rem;
    margin: 0.3rem;
    border-radius: 10px;
    background-color: #f3f4f6;
    text-align: center;
    border: 1px solid #d1d5db;
}
.metric-label { font-size: 0.75rem; color: #6b7280; }
.metric-value { font-size: 1.2rem; font-weight: bold; color: #111827; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📊 Dashboard Financiero - Estética Clara</h1>", unsafe_allow_html=True)

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
        wacc = ((e/v)*ke + (d/v)*kd*(1 -
