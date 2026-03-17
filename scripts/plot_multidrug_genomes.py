#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# Load data
# ======================
df_genes = pd.read_csv("amr_gene_presence.csv")  # genome-gene mapping
df_map = pd.read_csv("gene_antibiotic_class.csv")  # gene-class mapping

# ======================
# Merge gene presence with classes
# ======================
df_merged = df_genes.merge(df_map, on="Gene", how="left")

# Drop genes without a mapped class
df_merged = df_merged.dropna(subset=["Class"])

# Truncate genome name to accession number
df_merged["Genome"] = df_merged["Genome"].str.extract(r"(GC[AF]_\d+\.\d+)")
# ======================
# Count resistance classes per genome
# ======================
resistance_counts = df_merged.groupby("Genome")["Class"].nunique().sort_values(ascending=False)

# Save to CSV
resistance_counts.to_csv("resistance_count_per_genome.csv", header=True)

# ======================
# Plot horizontal bar chart
# ======================
top_n = 30
top_genomes = resistance_counts.head(top_n)

# Highlight top MDR genomes
highlight_n = 10
colors = ["red" if i < highlight_n else "steelblue" for i in range(len(top_genomes))]


plt.figure(figsize=(10,8))

ax = top_genomes[::-1].plot(  # reverse order so highest value appears at top
    kind="barh",
    color=colors[::-1]
)

# Add values at end of bars
for i, v in enumerate(top_genomes[::-1]):
    ax.text(v + 0.05, i, str(v), va="center")

plt.xlabel("Number of Resistance Classes")
plt.ylabel("Genome Accession")
plt.title(f"Top {top_n} Multidrug-Resistant Salmonella Genomes")

plt.tight_layout()
plt.savefig("multidrug-resistant_salmonella_genome", dpi=300)
plt.show()
