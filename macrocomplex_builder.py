# imports
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio import SeqIO, PDB, pairwise2
from Bio.PDB.Polypeptide import PPBuilder
import argparse, os, sys, UserInteraction

class Chain(object):
    """ DESCRIPTION """

    def __init__(self, sequence, file_index):
        self.__sequence = sequence
        self.__file_index = file_index

    def get_sequence(self):
        return self.__sequence

    def get_file_index(self):
        return self.__file_index

#main function that is called when running the script
if __name__ == "__main__":
    """ Macrocomplex builder based on structure superimposition."""
    
    # obtaining fasta and pdb files 
    
    fasta_files, pdb_files = UserInteraction.getUserInput()

# TODO: insert case of empty fasta file 
    seq_record_list = []
    for seq in fasta_files:
        for seq_record in SeqIO.parse(seq, "fasta"):
            seq_record_list.append(seq_record)

# TODO: insert case of empty pdb-file 
    parser = PDB.PDBParser()
    interact_structure = []
    for pdb_struct in pdb_files:
        interact_structure.append(parser.get_structure(pdb_struct,pdb_struct))
    print("interact structure", interact_structure)
    ppb = PPBuilder()
    pdb_seq = []
    for i in range(len(interact_structure)):
        for j in range(len(ppb.build_peptides(interact_structure[i]))):
            peptide = ppb.build_peptides(interact_structure[i])[j]
            # saves the record as a chain object with pdb-file index and sequence
            pdb_seq.append(Chain(peptide.get_sequence(), i))
    print("pdbseq:", pdb_seq)
    
    # for i in range(len(pdb_files)):
    #     for record in SeqIO.parse(pdb_files[i], "pdb-seqres"):
    #         # saves the record together with the index of the pdb file
    #         pdb_seq = pdb_seq.append([record,i])

# find the sequences that occur multiple times in pdb files and save all proteins for each structural aln in a separate list
sequences = []
for i in range(len(pdb_seq)):
    for m in range(i):
        # just check sequence alignments if sequences are not in the same pair
        if (pdb_seq[i].get_file_index() != pdb_seq[m].get_file_index()):
            print("Seq1:", pdb_seq[i].get_sequence())
            print("Seq2:", pdb_seq[i].get_sequence())
            # find the best alignment for two sequences (first element of list of alignments)
            alignment = pairwise2.align.globalxx(pdb_seq[i].get_sequence(), pdb_seq[m].get_sequence())[0]
            aln_seq_1 = alignment[0]
            aln_seq_2 = alignment[1]
            al_length = len(alignment[0])
            ident = sum(base1 == base2 for base1, base2 in zip(aln_seq_1, aln_seq_2))
    
            if ident/al_length >= 0.95:
                inserted = False
                for similar_seq in sequences:
                    if pdb_seq[i] in similar_seq:
                        similar_seq.append(pdb_seq[m])
                        inserted = True
                        break
                    elif pdb_seq[m] in similar_seq:
                        similar_seq.append(pdb_seq[i])
                        inserted = True
                        break
                if inserted == False: 
                    sequences.append([pdb_seq[i], pdb_seq[m]])
for i in range(len(sequences)):
    for el in sequences[i]:
        print("elem", i, el.get_file_index())

#def get_superimpose_options(chain_to_superimpose):

# do a structural alignment for all pdb files that contain an identity higher than 95%
def calcStrucAln():
    for i in range(len(similar_seq)):
        f = open('{}.domains'.format(i),"w+")
        for elem in similar_seq[i]:
            #access to pdb_file with certain index
            f.write(pdb_files[elem])
        f.close
        # do structural superposition with all pdb files that the index refers to
        # for using STAMP we need like globin.domains file

        #./2hhb.pdb 2hhba {CHAIN A}
        #./2hhb.pdb 2hhbb {CHAIN B}
        #./1lh1.pdb 1lh1 {ALL}
        #./2lhb.pdb 2lhb {ALL}
        #./4mbn.pdb 4mbn {ALL}
        #./1ecd.pdb 1ecd {ALL}



        # create file that contain all of the pdb files with the indexes

        # f= open("guru99.txt","w+")
        # for i in range(10):
        #   f.write("This is line %d\r\n" % (i+1))
        # f.close() 

        # install STAMP in our program?? as a dependency
        # then run STAMP

        return


# SET UP Superimposer
# TODO: How to save/output

# superimp = PDB.Superimposer()
# for l in range(len(similar_seq)):
#     for m in range(len(similar_seq[l])):
#         for n in range(m+1,len(similar_seq[l])):
#             if not similar_seq[l][m] == similar_seq[l][n]:
#                 superimp.set_atoms(pbd_seq[m], pdb_seq[n])
#                 print(superimp.rms)
# superimp.set_atoms(fixed, moving)
# superimp.rms
# superimp.apply(moving.get_atoms())
