from kegg_parser.kegg_kgml import KEGG
from kegg_parser.kegg_flat import KEGG_FLAT
import pandas as pd
import numpy as np

pathway = KEGG(KGML_file="./data/kgml/hsa05142.xml")

genes = pathway.node_attributes_df[pathway.node_attributes_df['type'] == 'gene']['name'].unique()
# Simulate RNA values
rna = pd.Series(data=np.random.normal(size=len(genes)), index=genes)
rna.head()

fig, axes = pathway.view(scale=2, show_compounds=False, gene_values=rna)
fig.savefig('hsa05142_reconstruct.png')


kegg_flat = KEGG_FLAT(KGML_file = "./data/flat/hsa05142.txt")
flat_file_results = kegg_flat.parse()

print(flat_file_results)
