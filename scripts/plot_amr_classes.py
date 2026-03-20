import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("amr_class_frequency.csv")
df.columns = ["Class", "Count"]

df.plot.bar(x="Class", y="Count", figsize=(10,6))

plt.title("Distribution of Antibiotic Resistance Classes in Salmonella")
plt.ylabel("Gene Count")
plt.xlabel("Antibiotic Class")

plt.tight_layout()
plt.savefig("figures/amr_class_distribution.png", dpi=300)

plt.show()
