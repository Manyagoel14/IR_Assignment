import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


adj = pd.read_csv("./Corpus2/adjacency_matrix.csv", index_col=0)
A = adj.values
titles = pd.read_excel("./Corpus2/papers.xlsx").iloc[:,2].astype(str).tolist()

pr_df = pd.read_csv("pagerank_scores.csv")
auth_df = pd.read_csv("hits_authority.csv")
hub_df = pd.read_csv("hits_hub.csv")

pr_scores_list = pr_df["score"].tolist()
auth_scores = dict(zip(auth_df["title"], auth_df["score"]))
hub_scores = dict(zip(hub_df["title"], hub_df["score"]))

G = nx.DiGraph()
for i,t in enumerate(titles):
    G.add_node(t)

for i in range(len(A)):
    for j in range(len(A)):
        if A[i][j] != 0:
            G.add_edge(titles[i], titles[j])

top5_auth = set(auth_df.sort_values("score", ascending=False).head(5)["title"].tolist())
top5_hub = set(hub_df.sort_values("score", ascending=False).head(5)["title"].tolist())

#color 
colors = []
for t in titles:
    if t in top5_auth and t in top5_hub:
        colors.append("purple")   #both
    elif t in top5_auth:
        colors.append("red")      #authorities
    elif t in top5_hub:
        colors.append("blue")     #hubs
    else:
        colors.append("gray")    

sizes = np.array(pr_scores_list)
sizes = ((sizes - sizes.min()) / (sizes.max() - sizes.min())) * 2000 + 300

pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(13,10))

nx.draw_networkx_nodes(
    G,
    pos,
    node_color=colors,
    node_size=sizes,
    alpha=0.9
)

nx.draw_networkx_edges(G, pos, arrowsize=10, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=7)

plt.title("Graph Network Visualization\nNode Size = PageRank   Colors = HITS Top Roles")
plt.axis("off")
plt.show()

