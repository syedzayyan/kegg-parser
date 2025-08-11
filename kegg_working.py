import marimo

__generated_with = "0.14.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r""" """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from kegg_zx.kegg import KEGG
    import pandas as pd
    import numpy as np
    return KEGG, np, pd


@app.cell
def _(KEGG):
    kegg_ins = KEGG(KGML_file="./data/kgml/hsa04024.xml")
    return (kegg_ins,)


@app.cell
def _(kegg_ins, np, pd):
    # Get genes in KEGG pathway
    genes = kegg_ins.node_attributes_df
    # Simulate RNA values
    rna = pd.Series(data=np.random.normal(size=len(genes)), index=genes)
    rna.head()
    return (rna,)


@app.cell
def _(kegg_ins, rna):
    kegg_ins.view(scale=2, show_compounds=True, gene_values=rna)
    return


@app.cell
def _(kegg_ins):
    G = kegg_ins.output_KGML_as_directed_networkx(genes_only=False)
    return (G,)


@app.cell
def _(G):
    for node in G.nodes(data  = True):
        print(node)
    return


@app.cell
def _(G):
    for edge in G.edges(data  = True):
        print(edge)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
