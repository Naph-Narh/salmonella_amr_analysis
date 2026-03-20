import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Load data
df_genes = pd.read_csv("amr_gene_presence.csv")
df_map = pd.read_csv("gene_antibiotic_class.csv")

df = df_genes.merge(df_map, on="Gene", how="left")
df = df.dropna(subset=["Class"])

# Genome → resistance classes
genome_classes = df.groupby("Genome")["Class"].unique()

# Node frequency (for size)
# -------------------------
class_freq = df["Class"].value_counts()

# Co-occurrence counts
pair_counts = {}

for classes in genome_classes:
    for pair in combinations(sorted(classes), 2):
        pair_counts[pair] = pair_counts.get(pair, 0) + 1

pairs_df = pd.DataFrame(
    [(a, b, w) for (a, b), w in pair_counts.items()],
    columns=["Class1", "Class2", "Weight"]
)

# keep stronger links
pairs_df = pairs_df[pairs_df["Weight"] >= 5]

# Build network
G = nx.Graph()

for _, row in pairs_df.iterrows():
    G.add_edge(row["Class1"], row["Class2"], weight=row["Weight"])

# Node size scaling
node_sizes = [class_freq[n]*50 for n in G.nodes()]

# Plot
plt.figure(figsize=(8,8))

pos = nx.spring_layout(G, seed=42, k=0.2)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=node_sizes,
    node_color="skyblue"
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=10
)

edges = G.edges(data=True)
weights = [e[2]["weight"] for e in edges]

nx.draw_networkx_edges(
    G,
    pos,
    width=[w*0.3 for w in weights],
    alpha=0.6,
    edge_color="gray",
    connectionstyle="arc3,rad=0.1"
)

edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=9
)

plt.title("Co-occurrence Network of Antibiotic Resistance Classes")
plt.axis("off")
plt.tight_layout()
plt.savefig("figures/amr_class_network.png", dpi=300)

plt.show()
