import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df_genes = pd.read_csv("amr_gene_presence.csv")          # Genome-Gene presence
df_map = pd.read_csv("gene_antibiotic_class.csv")        # Gene -> Class mapping

# Merge to get classes for each gene
df_merged = pd.merge(df_genes, df_map, on="Gene", how="left")

# Drop genes without a mapped class
df_merged = df_merged.dropna(subset=["Class"])

# Count total genes per class
class_counts = df_merged['Class'].value_counts()

# Convert to percentages
class_percent = class_counts / class_counts.sum() * 100

# Identify small classes (<2%)
small_classes = class_percent[class_percent < 3].index

# Save genes belonging to those classes
others_table = df_merged[df_merged["Class"].isin(small_classes)][["Gene","Class"]].drop_duplicates()
others_table.to_csv("amr_other_classes_table.csv", index=False)

# Group small classes into "Others"
class_counts_grouped = class_counts.copy()
others_sum = class_counts_grouped[small_classes].sum()

class_counts_grouped = class_counts_grouped.drop(small_classes)
class_counts_grouped["Others"] = others_sum

# Plot pie chart
plt.figure(figsize=(8,8))
plt.pie(
    class_counts_grouped,
    labels=class_counts_grouped.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.tab20.colors  # optional: nicer color palette
)
plt.title("Gene-Class Composition Across 100 Salmonella Genomes")
plt.tight_layout()
plt.savefig("amr_gene_class_composition.png", dpi=300)
plt.show()
