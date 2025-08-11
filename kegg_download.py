import marimo

__generated_with = "0.14.11"
app = marimo.App()


@app.cell
def _():
    import requests
    import xml.etree.ElementTree as ET
    from tqdm import tqdm  # progress bar
    import time
    import os
    import pandas as pd
    return ET, os, requests, time, tqdm


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Download KEGG""")
    return


@app.cell
def _(os):
    # Base folder
    base_dir = 'data'
    subdirs = ['kgml', 'flat', 'png']

    # Make subfolders
    for sub in subdirs:
        path = os.path.join(base_dir, sub)
        os.makedirs(path, exist_ok=True)
    return (base_dir,)


@app.cell
def _():
    url = 'http://rest.kegg.jp/link/hsa/pathway'
    return (url,)


@app.cell
def _(requests, url):
    response = requests.get(url)
    data = response.text
    return (data,)


@app.cell
def _(data):
    pathway_ids = sorted(set([line.split('\t')[0].replace('path:', '') for line in data.strip().split('\n')]))
    print(f"Found {len(pathway_ids)} unique pathways.")
    pathway_ids[:5]
    return (pathway_ids,)


@app.cell
def _():
    pathway_id = 'hsa00010'
    return (pathway_id,)


@app.cell
def _(pathway_id, requests):
    _kgml_url = f'http://rest.kegg.jp/get/{pathway_id}/kgml'
    kgml_text = requests.get(_kgml_url).text
    return (kgml_text,)


@app.cell
def _(kgml_text):
    kgml_text[:100]
    return


@app.cell
def _(ET, kgml_text):
    root = ET.fromstring(kgml_text)
    return (root,)


@app.cell
def _(root):
    entries = root.findall('entry')
    relations = root.findall('relation')
    return entries, relations


@app.cell
def _(entries, relations):
    print(f"Found {len(entries)} entries and {len(relations)} relations.")
    return


@app.cell
def _(base_dir, os, pathway_ids, requests, time, tqdm):
    for pid in tqdm(pathway_ids):
        kgml_path = os.path.join(base_dir, 'kgml', f'{pid}.xml')
        flat_path = os.path.join(base_dir, 'flat', f'{pid}.txt')
        png_path = os.path.join(base_dir, 'png', f'{pid}.png')
        if os.path.exists(kgml_path) and os.path.exists(flat_path) and os.path.exists(png_path):
            continue
        _kgml_url = f'http://rest.kegg.jp/get/{pid}/kgml'
        flat_url = f'http://rest.kegg.jp/get/{pid}'
        png_url = f'http://www.kegg.jp/kegg/pathway/hsa/{pid}.png'
        try:
            kgml_response = requests.get(_kgml_url)
            if kgml_response.ok:
                with open(kgml_path, 'w', encoding='utf-8') as _f:
                    _f.write(kgml_response.text)
            flat_response = requests.get(flat_url)
            if flat_response.ok:
                with open(flat_path, 'w', encoding='utf-8') as _f:
                    _f.write(flat_response.text)
            png_response = requests.get(png_url)
            if png_response.ok:
                with open(png_path, 'wb') as _f:
                    _f.write(png_response.content)
            time.sleep(0.2)
        except Exception as e:
            print(f'Error for {pid}: {e}')
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
