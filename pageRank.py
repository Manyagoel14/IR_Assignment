import pandas as pd
import numpy as np

E=0.15
data = pd.read_csv("corpus2/adjacency_matrix.csv")
data = data.iloc[:, 1:]

M = data.to_numpy(dtype=float)
n = M.shape[0]
col_sums = M.sum(axis=0)
col_sums[col_sums == 0] = 1
M = M / col_sums
print("Initital M:\n",M)

R = np.ones((n, 1)) / n
print("\nR0 Matrix:\n",R)

iterations=0
while True:
    M_new = E*M+(1 - E)/ n
    R_new=M_new@R
    iterations+=1
    if np.allclose(R, R_new, atol=1e-6):
        break
    R = R_new
print("\nFinal PageRank:\n", R)
l={}
for i in range(n):
    l[f"D{i+1}"]=float(R[i][0])

l_sorted = sorted(l.items(), key=lambda x: x[1], reverse=True)
paper_titles = pd.read_excel("./Corpus2/papers.xlsx")
paper_titles=paper_titles.iloc[:,[0,2]]   # id + col3
d=dict(paper_titles.values)

print("\nTop 5 PageRank:")
count=0
for key,val in l_sorted:
    print(f"{key}. {d[key]}: {val:.6f}")
    count+=1
    if count==5:
        break
print("\nNo. of iterations:",iterations)

#csv export
pr_list = []
for key,val in l.items():
    pr_list.append([d[key], val])
df_pr = pd.DataFrame(pr_list, columns=["title","score"])
df_pr.to_csv("pagerank_scores.csv", index=False)
print("\nPageRank scores saved to pagerank_scores.csv")