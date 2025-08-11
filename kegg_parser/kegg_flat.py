import re
from dataclasses import dataclass, field


@dataclass
class KEGG_FLAT_DATA:
    COMPOUNDS: list = field(default_factory=list)
    DRUGS: list = field(default_factory=list)
    GENE: list = field(default_factory=list)
    REFERENCE: dict = field(default_factory=dict)
    MODULE: list = field(default_factory=list)
    entry: str = field(default_factory=str)
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    kclass: str = field(default_factory=str)
    pathway_map: str = field(default_factory=str)
    dblinks: str = field(default_factory=str)
    organism: str = field(default_factory=str)


class KEGG_FLAT:
    def __init__(self, KGML_file=None):
        f = open(KGML_file, "r")
        file_contents = f.read()
        self.lines = iter(file_contents.splitlines())
        f.close()
        self.kegg_flat = KEGG_FLAT_DATA()

    def parse(self):
        for line in self.lines:
            if not line.startswith("/"):
                if not line.startswith(" "):
                    first_word = line.split(" ")[0]
                    if first_word.isupper() and first_word.replace("_", "").isalpha():
                        parsing = first_word
                proc_line = line.replace(parsing, "").strip()
                match parsing:
                    case "ENTRY":
                        self.kegg_flat.entry = proc_line
                    case "NAME":
                        self.kegg_flat.name = proc_line
                    case "DESCRIPTION":
                        self.kegg_flat.description = proc_line
                    case "CLASS":
                        self.kegg_flat.kclass = proc_line
                    case "PATHWAY_MAP":
                        self.kegg_flat.pathway_map = proc_line
                    case "MODULE":
                        pattern = r"^(hsa_\S+)\s+(.*)\s+(\[PATH:.*\])$"
                        match_module = re.match(pattern, proc_line)
                        module_things = match_module.groups()
                        self.kegg_flat.MODULE = module_things
                    case "DRUG":
                        self.kegg_flat.DRUGS = {
                            proc_line.split(" ")[0]: proc_line.split(" ")[2]
                        }
                    case "DBLINKS":
                        self.kegg_flat.dblinks = proc_line
                    case "ORGANISM":
                        self.kegg_flat.organism = proc_line
                    case "GENE":
                        number = gene = name = ko = ec = None
                        match = re.match(
                            r"^\s*(\d+)?\s*(\S+)?;\s*(.*?)\s*(?:\[(KO:[^\]]+)\])?\s*(?:\[(EC:[^\]]+)\])?\s*$",
                            proc_line,
                        )
                        number, gene, name, ko, ec = match.groups()
                        self.kegg_flat.GENE = [number, gene, name, ko, ec]
                    case "COMPOUND":
                        self.kegg_flat.COMPOUNDS = {
                            proc_line.split(" ")[0]: proc_line.split(" ")[2]
                        }
                    case "REFERENCE":
                        if proc_line.startswith("PMID"):
                            curr_pmid = proc_line
                            self.kegg_flat.REFERENCE[curr_pmid] = dict()
                        if proc_line.startswith("AUTHORS"):
                            self.kegg_flat.REFERENCE[curr_pmid]["authors"] = proc_line
                        if proc_line.startswith("TITLE"):
                            self.kegg_flat.REFERENCE[curr_pmid]["title"] = proc_line
                        if proc_line.startswith("JOURNAL"):
                            self.kegg_flat.REFERENCE[curr_pmid]["reference"] = proc_line
                        if proc_line.startswith("DOI"):
                            self.kegg_flat.REFERENCE[curr_pmid]["doi"] = proc_line
                    case "REL_PATHWAY":
                        print(proc_line)
                    case "KO_PATHWAY":
                        print(proc_line)
                    case _:
                        None
                return self.kegg_flat
