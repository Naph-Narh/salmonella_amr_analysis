import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load presence data
df = pd.read_csv("amr_gene_presence.csv")

# Truncate genome name to accession number
df["Genome"] = df["Genome"].str.extract(r"(GC[AF]_\d+\.\d+)")

# Pivot to matrix: genomes x genes
matrix = df.assign(Presence=1).pivot_table(index='Genome', columns='Gene', values='Presence', fill_value=0)

# Sort columns by total presence (most common first)
matrix = matrix[matrix.sum(axis=0).sort_values(ascending=False).index]

freq = pd.read_csv("amr_gene_frequency.csv")
freq.columns = ["Gene", "Count"]

# Plot heatmap
plt.figure(figsize=(12,8))
sns.heatmap(matrix, cmap="Reds", cbar_kws={'label': 'Presence'}, linewidths=0.5)
plt.savefig("figures/amr_gene_heatmap_clustered.png", dpi=300)

freq.plot.bar(x="Gene", y="Count", figsize=(12,6), color="tomato")
plt.title("AMR Gene Presence/Absence")
plt.ylabel("Genomes")
plt.xlabel("AMR Genes")
plt.tight_layout()
plt.savefig("figures/amr_gene_frequency_bar.png", dpi=300)
plt.show()
