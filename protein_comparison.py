import requests 
import json 
from sys import argv 

class Protein:
    """
    Class protein contains protein's sequence, id from Api and id from PDB
    """

class DataSourceApi: 
    """
    Class which connects to Api proteins base.
    Take path to file contains ids to download.
    Returns downloaded data with "yield".
    """

class DataSourcePDB():
    """
    Class which connects to PDB proteins base.
    Take id list contains ids to download.
    Returns downloaded data with "yield".
    """



class Protein:

    def __init__(self, sequence, api_id, pdb_id):
        self.sequence = sequence
        self.api_id = api_id
        self.pdb_id = pdb_id

    def __str__(self):
        return f'Object of class Protein with ABI ID {self.api_id},and PDB ID :{self.pdb_id}'

class DataSourceApi: 

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def __str__(self):
        return f'Data Source at path {self.path_to_file}'

    def __enter__(self):
        with open(self.path_to_file, 'rt') as data_file: #contains ids of proteins
            try:
                print("Downloading data from API database.")    
                for line in data_file:
                    uniprot_id = line.strip('\n').strip()
                    url = f'https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}' 
                    response = requests.get(url, headers={'Accept': 'application/json'}) 
                    if response.ok:
                        json_data = json.loads(response.text)
                        yield json_data
                print("Downloading ended succesfully")             
            except:
                print("Nope")
    def __exit__(self, exc, ext, tb):
        print("Done")


class DataSourcePDB: 


    def __init__(self, id_list):
        self.id_list = id_list

    def __str__(self):
        return f'Data Source from list: {self.id_list}'

    def __enter__(self):
        try:
            print("Downloading data from PDB database.")
            for line in self.id_list:
                pdb_id = line.strip('\n').strip()
                url = f'https://files.rcsb.org/view/{pdb_id}.pdb' #tworzymy poszczegolne adresy
                response = requests.get(url) #pobieramy dane spod linku 
                if response.ok:
                    yield response.text
            print("Downloading ended succesfully")             
        except:
            print("Nope")
    def __exit__(self, exc, ext, tb):
        print("Done")

def three_2_one(seq):
    """
    Takes string contains of 3-letter abbreviations of amino acids.
    Returns string contains of 1-letter abbreviations of amino acids.
    """
    new_seq = ''
    amino_dict = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
    for word in seq:
        new_seq += amino_dict[word]
    return new_seq


def finding_API(ds_1):
    """
    Takes data returned from DataSourceApi and searches for sequences, api_id and pdb_id.
    Returnes set of Protein type objects contains corresponding informations
    and list of PDB ids for searching in PDB database.
    """
    with ds_1 as datasource:
        for data in datasource:
            db_list = []
            api_id = data['accession']
            seq = data['sequence']['sequence']
            db_list = data['dbReferences']
            for record in db_list: #searching for PDB id
                if record['type'] == 'PDB':
                    protein_objects.append(Protein(seq, api_id, record['id']))#creating Protein type objects
                    break

    #creating list of PDB ids for searching in PDB database
    id_list = []
    for protein in protein_objects:
        id_list.append(protein.pdb_id) 
    return protein_objects, id_list

def finding_PDB(id_list):
    """
    Takes list of ids from finding_API and searches for corresponding sequences.
    Returnes set of sequences with 1-letter abbreviations.
    """
    ds_2 = DataSourcePDB(id_list)
    seq_list = []
    with ds_2 as datasource2:
        for data2 in datasource2:
            data2 = data2.split('\n')
            sum_sequence = ''
            for line in data2:
                if line.startswith('SEQRES'):
                    line = line.split()
                    chain_name = line[2]; sequence = line[4:]
                    if chain_name == 'A':
                        sum_sequence += three_2_one(sequence)
            seq_list.append(sum_sequence)
    return seq_list

def comparison(ABI_seq, PDB_seq):
    """
    Takes ABI and PDB sequence.
    Returns boolean if they are equal.
    """
    return ABI_seq == PDB_seq

if __name__ == '__main__':
    protein_objects = []
    protein_objects, id_list = finding_API(DataSourceApi(argv[1]))
    seq_list = finding_PDB(id_list)
    for i in range(len(seq_list)):
        print(f'Sequences from API and PDB for protein {protein_objects[i].api_id} are equal: ')
        print(comparison(protein_objects[i].sequence, seq_list[i]))
