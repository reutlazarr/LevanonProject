from Bio import Entrez, SeqIO

# Provide your email address to NCBI
Entrez.email = "reootlazar@gmail.com"

# Function to fetch the gene record by gene name
def fetch_gene_record(gene_name):
    handle = Entrez.esearch(db="nucleotide", term=gene_name, retmax=1)
    record = Entrez.read(handle)
    handle.close()
    if record["IdList"]:
        gene_id = record["IdList"][0]
        handle = Entrez.efetch(db="nucleotide", id=gene_id, rettype="gb", retmode="text")
        gene_record = SeqIO.read(handle, "genbank")
        handle.close()
        return gene_record
    else:
        return None

# Function to get the length of the gene
def get_gene_length(gene_name):
    gene_record = fetch_gene_record(gene_name)
    if gene_record:
        return len(gene_record.seq)
    else:
        return None

# # Example usage
# gene_name = "BRCA1"  # Replace with your gene name
# gene_length = get_gene_length(gene_name)
# if gene_length:
#     print(f"The length of the gene {gene_name} is {gene_length} bases.")
# else:
#     print(f"Gene {gene_name} not found.")
