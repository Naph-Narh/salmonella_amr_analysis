import pandas as pd

# Load gene presence data
genes = pd.read_csv("amr_gene_presence.csv")

# Load gene → antibiotic class mapping
mapping = pd.read_csv("gene_antibiotic_class.csv")

# Merge datasets
merged = genes.merge(mapping, on="Gene", how="left")

# Count genes per antibiotic class
class_counts = merged["Class"].value_counts()

# Save results
class_counts.to_csv("amr_class_frequency.csv")

print(class_counts)
