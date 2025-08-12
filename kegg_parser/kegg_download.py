import os
import requests
from tqdm.auto import tqdm

class KEGG_UTILITY:
    def __init__(self):
        pass
    def pathway_list_by_organism(self, organism = "hsa"):
        pathway_uri = f"https://rest.kegg.jp/link/{organism}/pathway"
        response = requests.get(pathway_uri)
        data = response.text
        pathway_ids = sorted(set([line.split('\t')[0].replace('path:', '') for line in data.strip().split('\n')]))
        return pathway_ids

    def download_single_file(self, pid, file_type = "kgml", file_path = "./data"):
        os.makedirs(file_path, exist_ok=True)
        match file_type:
            case "kgml":
                kgml_url = f'http://rest.kegg.jp/get/{pid}/kgml'
                response = requests.get(kgml_url)
            case "txt":
                flat_url = f'http://rest.kegg.jp/get/{pid}'
                response = requests.get(flat_url)
            case "png":
                png_url = f'http://www.kegg.jp/kegg/pathway/hsa/{pid}.png'
                response = requests.get(png_url)
            case _:
                 raise ValueError("Unsupported file type")
        if response.ok:
            file_path = os.path.join(file_path, f"{pid}.{file_type}")
            if file_type == "png":
                with open(file_path, 'wb') as _f:
                    _f.write(response.content)
            else:
                with open(file_path, 'w', encoding='utf-8') as _f:
                    _f.write(response.text)
        else:
            raise ValueError("Error Making Request")

    def download_files_for_single_organism(self, org = "hsa", type_file = "kgml", path = "./data"):
        pathway_ids = self.pathway_list_by_organism(org)
        for pid in tqdm(pathway_ids):
            self.download_single_file(pid, type_file, path)
