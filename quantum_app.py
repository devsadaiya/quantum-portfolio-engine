import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.optimize import minimize

st.set_page_config(page_title="Quantum Portfolio Engine", layout="wide", initial_sidebar_state="collapsed")


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@300;400;700;800&family=DM+Sans:wght@200;300;400&display=swap');

    body { background: #0a0a0a; color: #e2e2e2; }

    .stApp {
        background: #0a0a0a;
        color: #e2e2e2;
        font-family: 'DM Sans', sans-serif;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #e8c97d, #e2e2e2, #e8c97d, transparent);
        z-index: 9999;
    }

    /* Hide default streamlit header */
    header[data-testid="stHeader"] { background: transparent !important; }
    .stDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        color: #f0f0f0 !important;
        letter-spacing: -1px !important;
        line-height: 1.1 !important;
    }

    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 1.6rem !important; }
    h3 { font-size: 1.1rem !important; }

    p, .stMarkdown p {
        font-family: 'DM Sans', sans-serif !important;
        color: #666 !important;
        font-weight: 300 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px !important;
    }

    .stTextInput > div > div > input {
        background: #111 !important;
        border: 1px solid #222 !important;
        border-radius: 4px !important;
        color: #e2e2e2 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 300 !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px !important;
        padding: 14px 16px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
        caret-color: #e8c97d !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e8c97d66 !important;
        box-shadow: 0 0 0 3px #e8c97d0d !important;
    }
    .stTextInput label {
        color: #444 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 400 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
    }

    .stButton > button {
        background: #e8c97d !important;
        border: none !important;
        color: #0a0a0a !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        border-radius: 4px !important;
        padding: 12px 32px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: #f0d88e !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px #e8c97d33 !important;
    }

    /* Metric cards */
    .metric-card {
        background: #111;
        padding: 24px 28px;
        border-radius: 6px;
        border: 1px solid #1e1e1e;
        box-shadow: 0 4px 24px #00000055;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 12px;
    }
    .metric-card:hover {
        border-color: #e8c97d33;
        box-shadow: 0 8px 40px #00000077;
    }
    .metric-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        font-weight: 400;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #444;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #e8c97d;
        letter-spacing: -1px;
    }
    .metric-sub {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        color: #333;
        margin-top: 4px;
    }

    /* Section divider */
    .section-divider {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 48px 0 32px 0;
    }
    .section-divider .line {
        flex: 1;
        height: 1px;
        background: #1e1e1e;
    }
    .section-divider .label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #333;
    }

    /* Hero section */
    .hero-section {
        padding: 64px 0 48px 0;
        border-bottom: 1px solid #141414;
        margin-bottom: 48px;
    }
    .hero-tag {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #e8c97d;
        margin-bottom: 16px;
        display: block;
    }
    .hero-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #444;
        max-width: 480px;
        line-height: 1.7;
        font-weight: 300;
        margin-top: 16px;
    }

    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 40px;
        padding: 24px 0;
        border-top: 1px solid #141414;
        border-bottom: 1px solid #141414;
        margin: 32px 0;
    }
    .stat-item { display: flex; flex-direction: column; gap: 4px; }
    .stat-num {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: #e2e2e2;
    }
    .stat-desc {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #333;
    }

    /* Input zone */
    .input-zone {
        background: #0d0d0d;
        border: 1px solid #1a1a1a;
        border-radius: 8px;
        padding: 32px;
        margin: 32px 0;
    }

    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #1e1e1e !important;
        border-radius: 6px !important;
        overflow: hidden;
    }

    [data-testid="stSidebar"] {
        background: #080808 !important;
        border-right: 1px solid #1a1a1a !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #1e1e1e !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #333 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.7rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        padding: 12px 24px !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #e8c97d !important;
        border-bottom: 2px solid #e8c97d !important;
        background: transparent !important;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    .element-container {
        margin-bottom: 0 !important;
    }
    .appview-container .main .block-container {
        padding-top: 1rem !important;
    }
    .hero-section {
        padding: 32px 0 32px 0 !important;
    }
    .stats-bar {
        margin: 16px 0 !important;
    }

    ::-webkit-scrollbar { width: 3px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
    </style>
""", unsafe_allow_html=True)


PLOTLY_LAYOUT = dict(
    paper_bgcolor='#0d0d0d',
    plot_bgcolor='#0d0d0d',
    font=dict(family='DM Sans', color='#666', size=11),
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(gridcolor='#161616', linecolor='#1e1e1e', tickfont=dict(color='#444', size=10)),
    yaxis=dict(gridcolor='#161616', linecolor='#1e1e1e', tickfont=dict(color='#444', size=10)),
)

GOLD = '#e8c97d'
SILVER = '#a8a8a8'


st.markdown("""
<div class="hero-section">
    <span class="hero-tag">— DGen Analytics</span>
    <h1>Quantum Portfolio<br/>Analytics Engine</h1>
    <p class="hero-subtitle">
        Institutional-grade risk analytics, efficient frontier optimization,
        and correlation analysis — built for the modern investor.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <span class="stat-num">7yr</span>
        <span class="stat-desc">Data Window</span>
    </div>
    <div class="stat-item">
        <span class="stat-num">10k</span>
        <span class="stat-desc">MC Simulations</span>
    </div>
    <div class="stat-item">
        <span class="stat-num">7%</span>
        <span class="stat-desc">Risk-Free Rate</span>
    </div>
    <div class="stat-item">
        <span class="stat-num">Nifty 50</span>
        <span class="stat-desc">Benchmark Index</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-zone">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
   ticker_input = st.text_input("Stock Tickers", placeholder="RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS")
with col2:
    st.markdown("<br/>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze Portfolio")
st.markdown('</div>', unsafe_allow_html=True)

market_index = "^NSEI"
risk_free_rate = 0.07
start_date = "2018-01-01"
end_date = "2026-01-01"
N_SIMULATIONS = 10000

def compute_efficient_frontier(returns_df, n_simulations=N_SIMULATIONS, rf=risk_free_rate):
    mean_returns = (1 + returns_df.mean())**252 - 1
    cov_matrix = returns_df.cov() * 252
    n_assets = len(returns_df.columns)

    port_returns, port_vols, port_sharpes, port_weights = [], [], [], []

    for _ in range(n_simulations):
        w = np.random.dirichlet(np.ones(n_assets))
        r = np.dot(w, mean_returns)
        v = np.sqrt(w @ cov_matrix.values @ w)
        s = (r - rf) / v
        port_returns.append(r)
        port_vols.append(v)
        port_sharpes.append(s)
        port_weights.append(w)

    # Max Sharpe
    def neg_sharpe(w):
        r = np.dot(w, mean_returns)
        v = np.sqrt(w @ cov_matrix.values @ w)
        return -(r - rf) / v

    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [(0, 1)] * n_assets
    w0 = np.ones(n_assets) / n_assets
    opt_sharpe = minimize(neg_sharpe, w0, method='SLSQP', bounds=bounds, constraints=constraints)
    max_sharpe_weights = opt_sharpe.x

    # Min Volatility
    def portfolio_vol(w):
        return np.sqrt(w @ cov_matrix.values @ w)

    opt_vol = minimize(portfolio_vol, w0, method='SLSQP', bounds=bounds, constraints=constraints)
    min_vol_weights = opt_vol.x

    return (
        np.array(port_vols),
        np.array(port_returns),
        np.array(port_sharpes),
        np.array(port_weights),
        max_sharpe_weights,
        min_vol_weights,
        mean_returns,
        cov_matrix
    )

def plot_efficient_frontier(vols, rets, sharpes, weights, max_w, min_w, tickers, mean_returns, cov_matrix):
    max_r = np.dot(max_w, mean_returns)
    max_v = np.sqrt(max_w @ cov_matrix.values @ max_w)
    min_r = np.dot(min_w, mean_returns)
    min_v = np.sqrt(min_w @ cov_matrix.values @ min_w)

    fig = go.Figure()

    # Scatter cloud
    fig.add_trace(go.Scatter(
        x=vols * 100, y=rets * 100,
        mode='markers',
        marker=dict(
            color=sharpes,
            colorscale=[[0, '#1a1a1a'], [0.4, '#2a2a2a'], [0.7, '#8a7040'], [1.0, GOLD]],
            size=3,
            opacity=0.6,
            showscale=True,
            colorbar=dict(
                title=dict(text='Sharpe', font=dict(color='#444', size=10)),
                tickfont=dict(color='#444', size=9),
                thickness=8,
                len=0.6,
                bgcolor='#0d0d0d',
                bordercolor='#1e1e1e',
                borderwidth=1,
            )
        ),
        hovertemplate='<b>Vol:</b> %{x:.1f}%<br><b>Return:</b> %{y:.1f}%<extra></extra>',
        name='Simulated Portfolios'
    ))

    # Max Sharpe
    fig.add_trace(go.Scatter(
        x=[max_v * 100], y=[max_r * 100],
        mode='markers+text',
        marker=dict(color=GOLD, size=14, symbol='star', line=dict(color='#0a0a0a', width=1)),
        text=['Max Sharpe'], textposition='top right',
        textfont=dict(color=GOLD, size=10, family='DM Sans'),
        name='Max Sharpe',
        hovertemplate=f'<b>Max Sharpe</b><br>Vol: {max_v*100:.1f}%<br>Return: {max_r*100:.1f}%<extra></extra>'
    ))

    # Min Vol
    fig.add_trace(go.Scatter(
        x=[min_v * 100], y=[min_r * 100],
        mode='markers+text',
        marker=dict(color=SILVER, size=14, symbol='diamond', line=dict(color='#0a0a0a', width=1)),
        text=['Min Vol'], textposition='top right',
        textfont=dict(color=SILVER, size=10, family='DM Sans'),
        name='Min Volatility',
        hovertemplate=f'<b>Min Vol</b><br>Vol: {min_v*100:.1f}%<br>Return: {min_r*100:.1f}%<extra></extra>'
    ))

    # Individual stocks
    for ticker in tickers:
        s_r = mean_returns[ticker] * 100
        s_v = np.sqrt(cov_matrix.loc[ticker, ticker]) * 100
        fig.add_trace(go.Scatter(
            x=[s_v], y=[s_r],
            mode='markers+text',
            marker=dict(color='#2a2a2a', size=10, symbol='circle', line=dict(color='#444', width=1)),
            text=[ticker], textposition='top center',
            textfont=dict(color='#555', size=9, family='DM Sans'),
            showlegend=False,
            hovertemplate=f'<b>{ticker}</b><br>Vol: {s_v:.1f}%<br>Return: {s_r:.1f}%<extra></extra>'
        ))

    layout = PLOTLY_LAYOUT.copy()
    layout.update(dict(
        title=dict(text='Efficient Frontier — 10,000 Monte Carlo Simulations', font=dict(color='#333', size=11, family='DM Sans'), x=0),
        xaxis=dict(**PLOTLY_LAYOUT['xaxis'], title=dict(text='Annual Volatility (%)', font=dict(color='#333', size=10))),
        yaxis=dict(**PLOTLY_LAYOUT['yaxis'], title=dict(text='Annual Return (%)', font=dict(color='#333', size=10))),
        showlegend=True,
        legend=dict(
            font=dict(color='#444', size=9, family='DM Sans'),
            bgcolor='#111',
            bordercolor='#1e1e1e',
            borderwidth=1,
            x=0.02, y=0.98
        ),
        height=520,
    ))
    fig.update_layout(**layout)
    return fig

def plot_correlation_heatmap(returns_df):
    corr = returns_df.corr().round(2)
    tickers = list(corr.columns)

    # Custom colorscale: deep navy → dark → gold
    colorscale = [
        [0.0, '#0d1520'],
        [0.25, '#111a22'],
        [0.5, '#1a1a1a'],
        [0.75, '#6b5a2a'],
        [1.0, '#e8c97d'],
    ]

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=tickers,
        y=tickers,
        colorscale=colorscale,
        zmid=0,
        zmin=-1, zmax=1,
        text=corr.values,
        texttemplate='%{text}',
        textfont=dict(size=11, color='#888', family='DM Sans'),
        hoverongaps=False,
        hovertemplate='<b>%{x} × %{y}</b><br>Correlation: %{z:.2f}<extra></extra>',
        colorbar=dict(
            title=dict(text='ρ', font=dict(color='#444', size=12)),
            tickfont=dict(color='#444', size=9),
            thickness=8,
            len=0.8,
            bgcolor='#0d0d0d',
            bordercolor='#1e1e1e',
            borderwidth=1,
            tickvals=[-1, -0.5, 0, 0.5, 1],
        )
    ))

    layout = PLOTLY_LAYOUT.copy()
    layout.update(dict(
        title=dict(text='Correlation Matrix — Pairwise Return Correlation', font=dict(color='#333', size=11, family='DM Sans'), x=0),
        xaxis=dict(**PLOTLY_LAYOUT['xaxis'], side='bottom'),
        yaxis=dict(**PLOTLY_LAYOUT['yaxis'], autorange='reversed'),
        height=max(360, len(tickers) * 64),
    ))
    fig.update_layout(**layout)
    return fig

def plot_cumulative_returns(stock_data, market_data, stocks):
    fig = go.Figure()
    colors = [GOLD, '#a8a8a8', '#6b8fa8', '#7a8a6b', '#8a6b7a', '#6b7a8a']

    # Stocks
    for i, stock in enumerate(stocks):
        norm = (stock_data[stock] / stock_data[stock].iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=norm.index, y=norm.values,
            mode='lines',
            name=stock,
            line=dict(color=colors[i % len(colors)], width=1.5),
            hovertemplate=f'<b>{stock}</b><br>%{{y:.1f}}<extra></extra>'
        ))

    # Nifty 50
    norm_market = (market_data / market_data.iloc[0]) * 100
    fig.add_trace(go.Scatter(
        x=norm_market.index, y=norm_market.values.flatten(),
        mode='lines',
        name='nifty 50',
        line=dict(color='#2a2a2a', width=1.5, dash='dot'),
        hovertemplate='<b>S&P 500</b><br>%{y:.1f}<extra></extra>'
    ))

    layout = PLOTLY_LAYOUT.copy()
    layout.update(dict(
        title=dict(text='Cumulative Returns — Indexed to 100', font=dict(color='#333', size=11, family='DM Sans'), x=0),
        xaxis=dict(**PLOTLY_LAYOUT['xaxis'], title=None),
        yaxis=dict(**PLOTLY_LAYOUT['yaxis'], title=dict(text='Indexed Return', font=dict(color='#333', size=10))),
        showlegend=True,
        legend=dict(font=dict(color='#444', size=9, family='DM Sans'), bgcolor='#111', bordercolor='#1e1e1e', borderwidth=1),
        height=400,
        hovermode='x unified',
    ))
    fig.update_layout(**layout)
    return fig

if analyze_btn and ticker_input:
    stocks = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

    with st.spinner(""):
        try:
            stock_data = yf.download(stocks, start=start_date, end=end_date, auto_adjust=True)['Close']
            market_data = yf.download(market_index, start=start_date, end=end_date, auto_adjust=True)['Close']

            if isinstance(stock_data, pd.Series):
                stock_data = stock_data.to_frame(name=stocks[0])

            stock_returns = stock_data.pct_change().dropna(how='all')
            market_returns = market_data.pct_change().dropna().squeeze()
            stock_returns, market_returns = stock_returns.align(market_returns, join='inner', axis=0)

            # --- METRICS TABLE ---
            results = []
            for stock in stocks:
                if stock not in stock_returns.columns:
                    continue
                r = (1 + stock_returns[stock].mean())**252 - 1
                v = stock_returns[stock].std() * np.sqrt(252)
                combined = pd.concat([stock_returns[stock], market_returns], axis=1).dropna()
                beta = combined.iloc[:, 0].cov(combined.iloc[:, 1]) / combined.iloc[:, 1].var()
                sharpe = (r - risk_free_rate) / v
                results.append({'Ticker': stock, 'Annual Return': f"{r*100:.2f}%", 'Annual Vol': f"{v*100:.2f}%", 'Beta': f"{beta:.3f}", 'Sharpe Ratio': f"{sharpe:.3f}"})

            results_df = pd.DataFrame(results).set_index('Ticker')
            valid_stocks = [s for s in stocks if s in stock_returns.columns]

            # --- SECTION DIVIDER ---
            st.markdown("""
            <div class="section-divider">
                <div class="line"></div>
                <div class="label">Analysis Results</div>
                <div class="line"></div>
            </div>
            """, unsafe_allow_html=True)

            # --- SUMMARY METRICS ROW ---
            if valid_stocks:
                best_sharpe_row = max(results, key=lambda x: float(x['Sharpe Ratio']))
                best_return_row = max(results, key=lambda x: float(x['Annual Return'].replace('%','')))
                avg_beta = np.mean([float(r['Beta']) for r in results])

                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">Best Sharpe</div>
                        <div class="metric-value">{best_sharpe_row['Sharpe Ratio']}</div>
                        <div class="metric-sub">{best_sharpe_row['Ticker']}</div>
                    </div>""", unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">Top Return</div>
                        <div class="metric-value">{best_return_row['Annual Return']}</div>
                        <div class="metric-sub">{best_return_row['Ticker']}</div>
                    </div>""", unsafe_allow_html=True)
                with m3:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">Avg Portfolio Beta</div>
                        <div class="metric-value">{avg_beta:.2f}</div>
                        <div class="metric-sub">vs Nifty 50</div>
                    </div>""", unsafe_allow_html=True)
                with m4:
                    st.markdown(f"""<div class="metric-card">
                        <div class="metric-label">Assets Analyzed</div>
                        <div class="metric-value">{len(valid_stocks)}</div>
                        <div class="metric-sub">Valid tickers</div>
                    </div>""", unsafe_allow_html=True)

            # --- TABS ---
            tab1, tab2, tab3, tab4 = st.tabs(["Metrics", "Efficient Frontier", "Correlation", "Returns"])

            with tab1:
                st.markdown("<br/>", unsafe_allow_html=True)
                st.dataframe(results_df, use_container_width=True)

            with tab2:
                st.markdown("<br/>", unsafe_allow_html=True)
                if len(valid_stocks) >= 2:
                    clean_returns = stock_returns[valid_stocks].dropna()
                    vols, rets, sharpes, weights, max_w, min_w, mean_r, cov = compute_efficient_frontier(clean_returns)
                    fig_ef = plot_efficient_frontier(vols, rets, sharpes, weights, max_w, min_w, valid_stocks, mean_r, cov)
                    st.plotly_chart(fig_ef, use_container_width=True)

                    # Optimal weights
                    st.markdown("""
                    <div class="section-divider">
                        <div class="line"></div>
                        <div class="label">Optimal Allocations</div>
                        <div class="line"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Max Sharpe Portfolio**")
                        max_sharpe_val = -(minimize(lambda w: -(np.dot(w, mean_r) - risk_free_rate) / np.sqrt(w @ cov.values @ w),
                            np.ones(len(valid_stocks)) / len(valid_stocks), method='SLSQP',
                            bounds=[(0,1)]*len(valid_stocks), constraints={'type':'eq','fun':lambda w:sum(w)-1}).fun)
                        ms_df = pd.DataFrame({'Ticker': valid_stocks, 'Weight': [f"{w*100:.1f}%" for w in max_w]}).set_index('Ticker')
                        st.dataframe(ms_df, use_container_width=True)
                    with c2:
                        st.markdown("**Min Volatility Portfolio**")
                        mv_df = pd.DataFrame({'Ticker': valid_stocks, 'Weight': [f"{w*100:.1f}%" for w in min_w]}).set_index('Ticker')
                        st.dataframe(mv_df, use_container_width=True)
                else:
                    st.info("Enter at least 2 tickers to compute the efficient frontier.")

            with tab3:
                st.markdown("<br/>", unsafe_allow_html=True)
                if len(valid_stocks) >= 2:
                    fig_corr = plot_correlation_heatmap(stock_returns[valid_stocks])
                    st.plotly_chart(fig_corr, use_container_width=True)
                    st.markdown("""
                    <p style="color:#333; font-size:0.75rem; letter-spacing:0.5px; margin-top:8px;">
                    Values close to +1 indicate stocks move together — reducing diversification benefit.
                    Values near 0 or negative indicate uncorrelated or inversely correlated assets.
                    </p>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Enter at least 2 tickers for correlation analysis.")

            with tab4:
                st.markdown("<br/>", unsafe_allow_html=True)
                fig_ret = plot_cumulative_returns(stock_data[valid_stocks], market_data, valid_stocks)
                st.plotly_chart(fig_ret, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}. Please verify your ticker symbols.")

elif not ticker_input:
    # Empty state — decorative placeholder
    st.markdown("""
    <div style="margin-top: 48px; padding: 64px 48px; border: 1px solid #141414; border-radius: 8px; text-align: center;">
        <span style="font-family: 'DM Sans', sans-serif; font-size: 0.65rem; letter-spacing: 4px; text-transform: uppercase; color: #2a2a2a;">
            — Awaiting Input —
        </span>
        <h3 style="color: #1e1e1e !important; font-size: 2rem !important; margin: 24px 0 12px 0; letter-spacing: -1px;">
            Enter your tickers<br/>to begin analysis
        </h3>
        <p style="color: #222 !important; font-size: 0.8rem !important; max-width: 360px; margin: 0 auto; line-height: 1.8;">
            Efficient frontier · Correlation matrix · Sharpe optimization · Cumulative returns
        </p>
    </div>
    """, unsafe_allow_html=True)