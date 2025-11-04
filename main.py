# importing packages
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


CSV_PATH = "IR_Assignment/Corpus2/adjacency_matrix.csv"

# extracts labels and matrix 
def load_matrix(path):
    
    df = pd.read_csv(path, index_col=0)

    
    labels = list(df.index.astype(str))
    matrix = df.values

    return labels, matrix

def build_and_draw(labels, mat):
    G = nx.DiGraph()
    G.add_nodes_from(labels)
    n = len(labels)
    for i in range(n):
        for j in range(n):
            if int(mat[i, j]) != 0:
                G.add_edge(labels[i], labels[j])

    pos = nx.spring_layout(G, seed=1)            
    plt.figure(figsize=(10,10))
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='pink', edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=10)
    plt.title("Directed graph from adjacency matrix")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    labels, mat = load_matrix(CSV_PATH)
    print("Nodes:", labels)
    print("Adjacency shape:", mat.shape)
    build_and_draw(labels, mat)
