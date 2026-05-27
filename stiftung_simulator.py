import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="UHNW Familienstiftung Simulator")
st.title("Interactive Capital Stock Simulator: German Family Foundation")

# Sidebar Parameters
st.sidebar.header("Simulation Parameters")
cap_initial = st.sidebar.number_input("Initial Capital (€)", value=100000000, step=10000000)
years = st.sidebar.slider("Simulation Horizon (Years)", 5, 30, 15)
r_gross = st.sidebar.slider("Gross Annual Return (%)", 1.0, 12.0, 6.0) / 100
t_internal = st.sidebar.slider("Internal Foundation Tax Rate (%)", 0.5, 15.0, 1.5) / 100
inflation = st.sidebar.slider("Annual Inflation Rate (%)", 0.0, 8.0, 2.5) / 100
t_abgeltung = 0.26375 # Fixed German distribution tax + Soli

st.sidebar.header("Consumption Strategy (Net)")
cons_net_annual = st.sidebar.slider("Annual Net Consumption (€)", 500000, 5000000, 2000000, step=250000)

# Calculations
cons_month = cons_net_annual / 12
cons_day = cons_net_annual / 365
gross_distribution = cons_net_annual / (1 - t_abgeltung)

# Metrics Display
col1, col2, col3 = st.columns(3)
col1.metric("Net Consumption / Year", f"{cons_net_annual:,.0f} €")
col2.metric("Net Consumption / Month", f"{cons_month:,.0f} €")
col3.metric("Net Consumption / Day", f"{cons_day:,.0f} €")

# Simulation Loop
data = []
c_nominal = cap_initial
c_real = cap_initial

for year in range(1, years + 1):
    earnings = c_nominal * r_gross
    tax_inside = earnings * t_internal
    net_inside = earnings - tax_inside
    
    # Capital at end of year after distribution
    c_nominal = c_nominal + net_inside - gross_distribution
    c_real = c_nominal / ((1 + inflation) ** year)
    
    data.append({
        "Year": year,
        "Nominal Capital (€)": round(c_nominal, 2),
        "Real Capital (Inflation-adj, €)": round(c_real, 2),
        "Gross Distribution (€)": round(gross_distribution, 2)
    })

df = pd.DataFrame(data)

# Plotting
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Year"], y=df["Nominal Capital (€)"], name="Nominal Capital", line=dict(color='royalblue', width=3)))
fig.add_trace(go.Scatter(x=df["Year"], y=df["Real Capital (Inflation-adj, €)"], name="Real Capital (Inflation-Adjusted)", line=dict(color='firebrick', width=3, dash='dash')))
fig.update_layout(title="Capital Stock Progression Over Time", xaxis_title="Year", yaxis_title="Capital (€)", legend_title="Legend")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df.style.format("{:,.2f}"))
