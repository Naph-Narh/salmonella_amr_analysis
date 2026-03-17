import pandas as pd
import glob
import os

results_folder = "results"

files = glob.glob(results_folder + "/*_amr.txt")

data = []

for file in files:
    genome = os.path.basename(file).replace("_amr.txt","")
    
    df = pd.read_csv(file, sep="\t")
    
    if "Element symbol" in df.columns:
        genes = df["Element symbol"].dropna()
        
        for gene in genes:
            data.append({"Genome": genome, "Gene": gene})

combined = pd.DataFrame(data)

# Save full dataset
combined.to_csv("amr_gene_presence.csv", index=False)

# Only compute frequencies if genes exist
if not combined.empty:
    gene_counts = combined["Gene"].value_counts()
    gene_counts.to_csv("amr_gene_frequency.csv")
    print("AMR gene frequency file created")
else:
    print("No AMR genes detected in the genomes.")

print("Analysis complete")
