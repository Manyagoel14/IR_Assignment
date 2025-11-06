import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import network_plot as np_plot  

st.set_page_config(page_title="IR: PageRank & HITS Demo", layout="wide")

st.title("IR Assignment — PageRank & HITS Demo")
st.markdown(
    """
This small dashboard shows the top-ranked nodes by PageRank and HITS (authority/hub).
It also regenerates the network visualization dynamically.
"""
)

left, right = st.columns([1, 2])

PR_CSV = Path("pagerank_scores.csv")
AUTH_CSV = Path("hits_authority.csv")
HUB_CSV = Path("hits_hub.csv")

def safe_load(csv_path):
    if csv_path.exists():
        try:
            return pd.read_csv(csv_path)
        except Exception as e:
            st.error(f"Failed to read {csv_path}: {e}")
            return None
    else:
        st.warning(f"{csv_path} not found in repo root.")
        return None

pr_df = safe_load(PR_CSV)
auth_df = safe_load(AUTH_CSV)
hub_df = safe_load(HUB_CSV)


with left:
    st.header("Controls")
    labels_on = st.checkbox("Show node labels on graph", value=False)
    top_k = st.selectbox("Top-K to display", options=[5, 10], index=0)  # default Top 5
    refresh = st.button("Regenerate Plot")

with right:
    st.header("Top Rankings")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("PageRank (Top {})".format(top_k))
        if pr_df is not None:
            if pr_df.shape[1] >= 2:
                if "score" in pr_df.columns and any(c.lower() in ("title", "node", "name") for c in pr_df.columns):
                    title_col = [c for c in pr_df.columns if c.lower() in ("title", "node", "name")][0]
                    display_df = pr_df[[title_col, "score"]].sort_values("score", ascending=False).head(top_k)
                    display_df.columns = ["Title", "Score"]
                elif "score" in pr_df.columns and "title" not in pr_df.columns:
                    display_df = pr_df.sort_values("score", ascending=False).head(top_k)
                    display_df = display_df.reset_index().iloc[:, :2]
                    display_df.columns = ["Index", "Score"]
                else:
                    display_df = pr_df.sort_values(pr_df.columns[-1], ascending=False).head(top_k)
                    display_df.columns = ["Title", "Score"]
            else:
                display_df = pr_df.head(top_k)
            st.dataframe(display_df)
        else:
            st.write("pagerank_scores.csv not available.")

    with col2:
        st.subheader("Top Authorities (Top {})".format(top_k))
        if auth_df is not None:
            if auth_df.shape[1] >= 2:
                df = auth_df.sort_values(by=auth_df.columns[1], ascending=False).head(top_k)
                df = df.reset_index(drop=True)
                df.columns = ["Title", "Score"]
                st.dataframe(df)
            else:
                st.dataframe(auth_df.head(top_k))
        else:
            st.write("hits_authority.csv not available.")

    with col3:
        st.subheader("Top Hubs (Top {})".format(top_k))
        if hub_df is not None:
            if hub_df.shape[1] >= 2:
                df = hub_df.sort_values(by=hub_df.columns[1], ascending=False).head(top_k)
                df = df.reset_index(drop=True)
                df.columns = ["Title", "Score"]
                st.dataframe(df)
            else:
                st.dataframe(hub_df.head(top_k))
        else:
            st.write("hits_hub.csv not available.")

st.markdown("---")
st.header("Network Visualization")

plot_col1, plot_col2 = st.columns([3, 1])

with plot_col1:
    if refresh or True:
        try:
            fig = np_plot.create_network_plot(labels_on=labels_on, save_path=None)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Failed to create plot dynamically: {e}")
            fallback = Path("network_plot.png")
            if fallback.exists():
                st.image(str(fallback), caption="Saved network_plot.png")
            else:
                st.write("No plot available.")

with plot_col2:
    st.write("Legend")
    st.markdown(
        """
- **Red** = Top Authorities  
- **Blue** = Top Hubs  
- **Purple** = Both Hub + Authority  
- **Size** = PageRank (bigger → higher PR)
"""
    )

st.markdown("---")
st.caption("Files read from repo root: pagerank_scores.csv, hits_hub.csv, hits_authority.csv. Network data from Corpus2/*.")
