# 🧠 IR Assignment  
## Ranking Webpages and Influencers using PageRank and HITS  

Applying **link analysis algorithms (PageRank and HITS)** to identify important and influential entities in a network of documents.

---

## 📚 Table of Contents  
- [Features](#features)  
- [Installation](#installation)  
- [Screenshots](#screenshots)  
- [Contributors](#contributors)  

---

## 🚀 Features  

### Define the Corpus and Adjacency Matrix  
- Construct a **corpus** consisting of research papers (or documents) as nodes.  
- Define an **adjacency matrix** representing the citation or reference relationships between these nodes, where each entry `A[i][j]` indicates a directed link from node *i* to node *j*.  

### Graph Construction  
- Use the corpus and adjacency matrix to form a **directed graph**, where nodes represent papers and edges represent citation or influence links.  

### Algorithm Implementation  
- Apply the following graph-based algorithms to analyze node importance:  
  - **PageRank**  
  - **HITS (Hyperlink-Induced Topic Search)**  

### Data Export  
- Save the resulting data into a `.csv` file for further analysis or visualization.  

### Visualization Using Streamlit  
- Develop a **Streamlit application** to visualize the results:  
  - Display a table of top-ranked papers.  
  - Render a directed graph where:  
    - The **size** of each node is proportional to its **PageRank value**.  
    - The **color** of each node is determined by its **HITS (authority or hub) score**.  

---

## ⚙️ Installation  

1. Clone the repository  
   ```bash
   git clone https://github.com/Manyagoel14/IR_Assignment.git
