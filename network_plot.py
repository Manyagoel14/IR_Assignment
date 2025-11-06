# network_plot.py
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def create_network_plot(
    adjacency_path="./Corpus2/adjacency_matrix.csv",
    papers_path="./Corpus2/papers.xlsx",
    pagerank_csv="pagerank_scores.csv",
    hits_auth_csv="hits_authority.csv",
    hits_hub_csv="hits_hub.csv",
    labels_on=False,
    save_path=None,
    figsize=(13, 10),
    seed=42,
):
    """
    Build and return a matplotlib Figure showing the directed network.
    - labels_on: whether to show node labels (your UI asked labels OFF by default)
    - save_path: if provided, the figure will be saved to this path (PNG or other supported).
    Returns: matplotlib.figure.Figure
    """
   
    adj = pd.read_csv(adjacency_path, index_col=0)
    A = adj.values
    titles = pd.read_excel(papers_path).iloc[:, 2].astype(str).tolist()

    pr_df = pd.read_csv(pagerank_csv)
    auth_df = pd.read_csv(hits_auth_csv)
    hub_df = pd.read_csv(hits_hub_csv)

    if "score" in pr_df.columns:
        pr_scores_list = pr_df["score"].tolist()
    else:       
        pr_scores_list = pr_df.iloc[:, 0].tolist()


    auth_scores = dict(zip(auth_df.iloc[:, 0], auth_df.iloc[:, 1])) if auth_df.shape[1] >= 2 else dict()
    hub_scores = dict(zip(hub_df.iloc[:, 0], hub_df.iloc[:, 1])) if hub_df.shape[1] >= 2 else dict()

    # --- graph build ---
    G = nx.DiGraph()
    for t in titles:
        G.add_node(t)

    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] != 0:
                # source = titles[i], target = titles[j]
                G.add_edge(titles[i], titles[j])

    # --- identify top5 hubs / authorities ---
    top5_auth = set(auth_df.sort_values(by=auth_df.columns[1], ascending=False).head(5).iloc[:, 0].tolist())
    top5_hub = set(hub_df.sort_values(by=hub_df.columns[1], ascending=False).head(5).iloc[:, 0].tolist())

    # --- colors (visual roles) ---
    colors = []
    for t in titles:
        if t in top5_auth and t in top5_hub:
            colors.append("purple")   # both
        elif t in top5_auth:
            colors.append("red")      # authorities
        elif t in top5_hub:
            colors.append("blue")     # hubs
        else:
            colors.append("gray")

    # --- sizes from pagerank ---
    sizes = np.array(pr_scores_list[: len(titles)]) if len(pr_scores_list) >= len(titles) else np.array(pr_scores_list)
    # guard: if sizes length mismatch, pad or trim
    if sizes.size < len(titles):
        sizes = np.pad(sizes, (0, len(titles) - sizes.size), constant_values=sizes.min() if sizes.size>0 else 0.0)
    sizes = ((sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-12)) * 2000 + 300

    pos = nx.spring_layout(G, seed=seed)

    # create figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=colors,
        node_size=sizes,
        alpha=0.9,
        ax=ax,
    )

    nx.draw_networkx_edges(G, pos, arrowsize=10, alpha=0.5, ax=ax)

    if labels_on:
        nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)

    ax.set_title("Graph Network Visualization\nNode Size = PageRank   Colors = HITS Top Roles")
    ax.axis("off")

    # add simple legend
    # draw proxy artists for legend
    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D([0], [0], marker="o", color="w", label="Top Authority", markerfacecolor="red", markersize=10),
        Line2D([0], [0], marker="o", color="w", label="Top Hub", markerfacecolor="blue", markersize=10),
        Line2D([0], [0], marker="o", color="w", label="Both (Hub+Auth)", markerfacecolor="purple", markersize=10),
        Line2D([0], [0], marker="o", color="w", label="Others", markerfacecolor="gray", markersize=8),
    ]
    ax.legend(handles=legend_elements, loc="lower left")

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


if __name__ == "__main__":
    # if run directly, create and show + save
    fig = create_network_plot(save_path="network_plot.png", labels_on=True)
    plt.show()
