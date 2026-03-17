import pandas as pd

df = pd.read_csv("amr_gene_presence.csv")

counts = df.groupby("Genome")["Gene"].count().sort_values(ascending=False)

counts.to_csv("amr_genes_per_genome.csv")

print(counts.head(10))
