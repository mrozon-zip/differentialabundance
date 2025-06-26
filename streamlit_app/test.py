import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def is_docker():
    return os.path.exists('/.dockerenv')

local = not is_docker()
docker = is_docker()

if local:
    source = '../differentialabundance/test/'
elif docker:
    source = 'data/'

gsea = find('*gsea_report_for_*.tsv', f"{source}report/gsea/")

tables_differential = find('*deseq2.results.tsv', f"{source}tables/differential/")

tables_annotation = find('**.tsv', f"{source}tables/annotation")

print(f"gsea{gsea}\n\
      tables_annotation{tables_annotation}\n\
        tables_differential{tables_differential}\n")