import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load files
df_genes = pd.read_csv("amr_gene_presence.csv")
df_map = pd.read_csv("gene_antibiotic_class.csv")

# Normalize gene names
df_genes['Gene_norm'] = df_genes['Gene'].str.replace('Δ', 'delta', regex=False).str.strip()
df_map['Gene_norm'] = df_map['Gene'].str.replace('Δ', 'delta', regex=False).str.strip()

# Merge gene presence with drug classes
df_merged = df_genes.merge(df_map[['Gene_norm','Class']], on='Gene_norm', how='left')

# Check for unmapped genes
unmapped = df_merged[df_merged['Class'].isna()]['Gene'].unique()
if len(unmapped) > 0:
    print("Warning: Some genes were not mapped to any class:", unmapped)

# Create binary presence/absence table
df_classes = df_merged.pivot_table(index='Genome', columns='Class', aggfunc='size', fill_value=0)

# Take top 50 genomes by total number of resistance classes
top50 = df_classes.sum(axis=1).sort_values(ascending=False).head(50).index
df_top50 = df_classes.loc[top50]

# Shorten genome labels to accession only
df_top50.index = df_top50.index.str.split('_').str[0] + '_' + df_top50.index.str.split('_').str[1]

# Plot clustered heatmap
sns.set(font_scale=1.0)
g = sns.clustermap(
    df_top50,
    cmap="Greys",
    vmin=0,
    vmax=1,
    figsize=(12,8),
    linewidths=0.3,
    cbar_kws={"label": "Resistance Presence", "ticks": [0, 1], "shrink": 0.1
    }
)

g.cax.set_yticklabels(['Absent', 'Present'])
g.cax.yaxis.set_label_position('left')
g.cax.set_position([0.03, 0.05, 0.01, 0.18]) 
# [left, bottom, width, height] in figure coordinates (0 to 1)

plt.savefig("figures/amr_classes_per_genome.png", dpi=300)
plt.show()
