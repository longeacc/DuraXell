import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

from core.metrics import DEMO_METRICS, compute_routing, ROUTING_COLORS

st.set_page_config(page_title="Dashboard Métriques L2", page_icon="📊", layout="wide")

def load_data() -> pd.DataFrame:
    """Charge les données des métriques dans un DataFrame depuis la session."""
    rows = []
    # On itère sur les custom_metrics qui peuvent avoir été modifiées
    for entity, metrics in st.session_state.custom_metrics.items():
        if entity in st.session_state.selected_entities:
            row = {"Entity": entity}
            row.update(metrics)
            # Calcul du routage en temps réel basé sur les métriques et les seuils
            routing = compute_routing({k: v for k, v in row.items() if k != "Entity"}, st.session_state.thresholds)
            st.session_state.routings[entity] = routing
            row["Routing"] = routing
            rows.append(row)
    return pd.DataFrame(rows)

def render_sidebar_sliders() -> None:
    """Affiche les sliders des seuils pour les métriques L2 dans la sidebar."""
    st.sidebar.header("🎯 Seuils de Décision")
    
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Mode Frugal"):
        st.session_state.thresholds = {
            "Te": 0.50, "He": 0.45, "R": 0.60,
            "Freq": 0.20, "Yield": 0.40, "Feas": 0.30,
            "DomainShift": 0.45, "LLM_Necessity": 0.85
        }
    if col2.button("Mode Qualité"):
        st.session_state.thresholds = {
            "Te": 0.85, "He": 0.80, "R": 0.85,
            "Freq": 0.60, "Yield": 0.75, "Feas": 0.80,
            "DomainShift": 0.75, "LLM_Necessity": 0.50
        }

    st.sidebar.markdown("---")
    
    thresholds = st.session_state.thresholds
    
    st.sidebar.subheader("Niveau 1 : Règles")
    thresholds["Te"] = st.sidebar.slider("Templateability (Te)", 0.0, 1.0, thresholds["Te"], 0.01)
    thresholds["He"] = st.sidebar.slider("Homogeneity (He)", 0.0, 1.0, thresholds["He"], 0.01)
    thresholds["R"] = st.sidebar.slider("Rule Performance (R)", 0.0, 1.0, thresholds["R"], 0.01)
    
    st.sidebar.subheader("Niveau 2 : CRF")
    thresholds["Freq"] = st.sidebar.slider("Frequency (Freq)", 0.0, 1.0, thresholds["Freq"], 0.01)
    thresholds["Yield"] = st.sidebar.slider("Yield", 0.0, 1.0, thresholds["Yield"], 0.01)
    
    st.sidebar.subheader("Niveau 3 : Transformer")
    thresholds["DomainShift"] = st.sidebar.slider("Domain Shift (DS)", 0.0, 1.0, thresholds["DomainShift"], 0.01)
    thresholds["Feas"] = st.sidebar.slider("Feasibility (Feas)", 0.0, 1.0, thresholds["Feas"], 0.01)
    
    st.sidebar.subheader("Niveau 4 : LLM")
    thresholds["LLM_Necessity"] = st.sidebar.slider("LLM Necessity", 0.0, 1.0, thresholds["LLM_Necessity"], 0.01)

def plot_radar(df: pd.DataFrame, entity: str) -> go.Figure:
    """Génère un radar chart pour une entité spécifique comparée aux seuils."""
    tdf = df[df["Entity"] == entity].iloc[0]
    metrics_keys = ["Te", "He", "R", "Freq", "Yield", "DS", "Feas", "LLM_N"]
    
    # Mapper exact key names to display
    map_k = {"DS": "DomainShift", "LLM_N": "LLM_Necessity"}
    
    actual_vals = [tdf[map_k.get(k, k)] for k in metrics_keys]
    threshold_vals = [st.session_state.thresholds[map_k.get(k, k)] for k in metrics_keys]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=actual_vals,
        theta=metrics_keys,
        fill='toself',
        name=f"Metrics {entity}",
        line=dict(color=ROUTING_COLORS.get(tdf["Routing"], "#000"))
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=threshold_vals,
        theta=metrics_keys,
        name="Seuils actuels",
        line=dict(color='grey', dash='dot')
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title=f"Profil L2 : {entity} → {tdf['Routing']}"
    )
    return fig

def plot_heatmap(df: pd.DataFrame) -> go.Figure:
    """Affiche une heatmap de toutes les entités vs métriques L2."""
    metrics_cols = ["Te", "He", "R", "Freq", "Yield", "Feas", "DomainShift", "LLM_Necessity", "C"]
    df_hm = df.set_index("Entity")[metrics_cols]
    fig = px.imshow(
        df_hm,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        title="Matrice des Métriques par Entité"
    )
    return fig

def plot_distribution(df: pd.DataFrame) -> go.Figure:
    """Affiche la distribution des routages."""
    dist = df["Routing"].value_counts().reset_index()
    dist.columns = ["Routing", "Count"]
    
    fig = px.bar(
        dist, x="Routing", y="Count",
        color="Routing",
        color_discrete_map=ROUTING_COLORS,
        title="Répartition Cascade",
        category_orders={"Routing": ["RULES", "CRF", "TRANSFORMER", "LLM"]}
    )
    return fig

def plot_scatter(df: pd.DataFrame) -> go.Figure:
    """Affiche le scatter plot Coût vs Bénéfice(Perf moyenne R, Yield)."""
    df["Performance"] = (df["R"] + df["Yield"]) / 2
    fig = px.scatter(
        df, x="C", y="Performance",
        size="Freq", color="Routing",
        hover_name="Entity",
        color_discrete_map=ROUTING_COLORS,
        title="Analyse Coût / Performance L2",
        range_x=[0, 1.1], range_y=[0, 1.1]
    )
    return fig

def main() -> None:
    st.title("📊 Dashboard des Métriques L2")
    
    render_sidebar_sliders()
    
    if "selected_entities" not in st.session_state or not st.session_state.selected_entities:
        st.warning("Aucune entité sélectionnée. Allez dans REST Integration.")
        return
        
    # Initialisation de custom_metrics si non présent (fallback si on atterrit direct ici)
    if "custom_metrics" not in st.session_state:
        st.session_state.custom_metrics = {k: v.copy() for k, v in DEMO_METRICS.items()}
        
    df = load_data()
    
    def highlight_routing(val: str) -> str:
        color = ROUTING_COLORS.get(val, "black")
        return f'color: white; background-color: {color}'
        
    styled_df = df.style.map(highlight_routing, subset=['Routing'])
    
    st.subheader("Résumé analytique multi-couches (Éditable)")
    st.info("💡 **Conseil :** Modifiez les valeurs des métriques dans ce tableau pour voir la cascade être recalculée en temps réel !")
    
    edited_df = st.data_editor(
        styled_df,
        use_container_width=True,
        hide_index=True,
        disabled=["Entity", "Routing", "C"],
        key="metrics_editor"
    )
    
    # Synchronisation des modifs
    for i, row in edited_df.iterrows():
        ent = row["Entity"]
        for col in ["Te", "He", "R", "Freq", "Yield", "DS", "Feas", "LLM_N", "DomainShift", "LLM_Necessity"]:
            if col in row and not pd.isna(row[col]):
                # Mapping mapping possible du dataframe columns into the original keys
                mapped_col = col
                if col == "DS":
                    mapped_col = "DomainShift"
                elif col == "LLM_N":
                    mapped_col = "LLM_Necessity"
                
                # Mise à jour si changement
                if mapped_col in st.session_state.custom_metrics[ent]:
                    st.session_state.custom_metrics[ent][mapped_col] = float(row[col])

    # Re-calcul du dataframe avec les nouvelles metriques pour la suite
    df = load_data()

    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Export CSV", csv, "metrics_summary.csv", "text/csv")
    with col2:
        jsn = df.to_json(orient="records")
        st.download_button("Export JSON", jsn, "metrics_summary.json", "application/json")

    st.markdown("---")
    
    # Vues Graphiques
    tab1, tab2, tab3 = st.tabs(["Radar Profile", "Analyse Globale (Heatmap)", "Coût/Bénéfice"])
    
    with tab1:
        entity_to_plot = st.selectbox("Sélectionner une entité", df["Entity"].tolist())
        if entity_to_plot:
            st.plotly_chart(plot_radar(df, entity_to_plot), use_container_width=True)
            
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(plot_heatmap(df), use_container_width=True)
        with c2:
            st.plotly_chart(plot_distribution(df), use_container_width=True)
            
    with tab3:
        st.plotly_chart(plot_scatter(df), use_container_width=True)

if __name__ == "__main__":
    main()