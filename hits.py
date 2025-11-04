import numpy as np
import pandas as pd

CSV_PATH = "./Corpus2/adjacency_matrix.csv"
PAPER_PATH = "./Corpus2/papers.xlsx"

def load_matrix(path):
    df = pd.read_csv(path, index_col=0)
    labels = list(df.index)
    A = df.values.astype(float)
    return labels, A

def load_titles(path):
    df = pd.read_excel(path)
    return df.iloc[:,2].astype(str).tolist()

def print_table(titles, auth, hub, heading):
    df = pd.DataFrame({
        "Title": titles,
        "Authority Score": np.round(auth, 6),
        "Hub Score": np.round(hub, 6)
    })
    print("\n" + heading + "\n")
    print(df.to_string(index=False))


def hits(A, con = 0.0001, max_iter=1000):
    n = A.shape[0]
    auth = np.ones(n)
    hub = np.ones(n)

    auth = auth/np.linalg.norm(auth)
    hub = hub/np.linalg.norm(hub)

    initial_auth = auth.copy()
    initial_hub = hub.copy()

    for i in range(max_iter):
        new_auth = A.T.dot(hub)
        new_hub = A.dot(new_auth)

        new_auth = new_auth/np.linalg.norm(new_auth)
        new_hub = new_hub/np.linalg.norm(new_hub)

        if np.allclose(auth, new_auth, atol=con) and np.allclose(hub, new_hub, atol=con):
            return initial_auth, initial_hub, new_auth, new_hub, i+1

        auth=new_auth
        hub=new_hub

    return initial_auth,initial_hub,auth, hub, max_iter

if __name__ == "__main__":
    labels, A = load_matrix(CSV_PATH)
    titles = load_titles(PAPER_PATH)

    init_auth, init_hub, final_auth, final_hub, iterations = hits(A)
    print_table(titles, init_auth, init_hub, "Initial Scores")
    print(f"\nConverged in {iterations} iterations\n")
    print_table(titles, final_auth, final_hub, "Final Scores")

    top_auth_idx = np.argsort(-final_auth)[:5]
    top_hub_idx = np.argsort(-final_hub)[:5]
    print("\nTop 5 Authorities:")
    for i in top_auth_idx:
        print(titles[i], ":", final_auth[i])
    print("\nTop 5 Hubs:")
    for i in top_hub_idx:
        print(titles[i], ":", final_hub[i])
