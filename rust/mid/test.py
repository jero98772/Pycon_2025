import bioalgorithms
import time
from functools import wraps

def time_function(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(f"Function '{func.__name__}' took {end - start:.6f} seconds")
    return result

def levenshtein_distance(str1, str2):
    """
    Compute the Levenshtein edit distance between two strings.
    
    Parameters
    ----------
    str1 : str
        First string.
    str2 : str
        Second string.
    
    Returns
    -------
    int
        The number of single‑character edits (insertions, deletions,
        or substitutions) required to change `str1` into `str2`.
    """
    len1, len2 = len(str1), len(str2)

    # Create (len1+1) × (len2+1) matrix filled with zeros
    matrix: List[List[int]] = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Initialize first column and first row
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j

    # Populate the matrix
    for i, char1 in enumerate(str1):
        for j, char2 in enumerate(str2):
            cost = 0 if char1 == char2 else 1
            matrix[i + 1][j + 1] = min(
                matrix[i][j + 1] + 1,      # deletion
                matrix[i + 1][j] + 1,      # insertion
                matrix[i][j] + cost        # substitution
            )

    return matrix[len1][len2]


time_function(bioalgorithms.levenshtein_distance,"kitten","sitting")
time_function(levenshtein_distance,"kitten","sitting")

"""
print(bioalgorithms.levenshtein_distance("kitten","sitting"))
print(bioalgorithms.sequence_aligment("AGGGCT","AGGCA",3,2))
print(bioalgorithms.longest_commons_subsequences(["ACCGAAGG","ACCGAACC","CCACCGAAGG","GGACCGAACC"]))
print(bioalgorithms.longest_common_subsequence("ACCGAAGG","ACCGAACC"))
print(bioalgorithms.commun_patters(["XAaXV","XAsXV","XAcXV"]))
print(bioalgorithms.reconstruct_from_kmers(3,["AAT","ATG", "TGC", "GCT", "CTA"]))#check this output
print(bioalgorithms.translate_rna_to_aminoacid("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"))
print(bioalgorithms.de_bruijn_collection(["ATG", "ATG", "TGT", "TGG", "CAT", "GGA", "GAT", "AGA"], lambda kmer: kmer[:-1], lambda kmer: kmer[1:]))
print(bioalgorithms.find_eulerian_cycle({"AAT": ["ATG"],"ATG": ["TGC"],"TGC": ["GCT"],"GCT": ["CTA"],"CTA": ["TAC"],"TAC": ["ACG"],"ACG": ["CGA"],"CGA": ["GAT"],"GAT": ["ATG"]}))
print(bioalgorithms.de_bruijn(3, "ATGATCAAG"))
print(bioalgorithms.grph_kmers(["ACCGA", "CCGAA", "CGAAG", "GAAGC", "AAGCT"]))
print(bioalgorithms.reconstruct(["ACCGA", "CCGAA", "CGAAG", "GAAGC", "AAGCT"]))
print(bioalgorithms.kmer_composition(2,'CAATCCAAC'))
print(bioalgorithms.distance_between_pattern_and_strings("AA",['AAATTGACGCAT','GACGAAAAACGTT','CGTCAGCGCCTG''GCTGAGCAAAGG','AGTACGGGACAG']))
print(bioalgorithms.gibbs(4, 5, 10,["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"],1000))
print(bioalgorithms.randomized_motif_search(3,5,["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"],1))
print(bioalgorithms.greedy_motif_search(3,5,["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"]))
print(bioalgorithms.most_probable("ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT",5,[[0.2, 0.2, 0.3, 0.2, 0.3],[0.4, 0.3, 0.1, 0.5, 0.1],[0.3, 0.3, 0.5, 0.2, 0.4],[0.1, 0.2, 0.1, 0.1, 0.2]]))
print(bioalgorithms.median_string(['AAATTGACGCAT','GACGACCACGTT','CGTCAGCGCCTG''GCTGAGCACCGG','AGTACGGGACAG'],6))
print(bioalgorithms.enumerate_motifs(["ATTTGGC","TGCCTTA","CGGTATC","GAAAATT"],3,1))
print(bioalgorithms.pattern_to_number("CC"))
print(bioalgorithms.number_to_pattern(5,2))
print(bioalgorithms.generate_frequency_array("AAACAGATCACCCGCTGAGCGGGTTATCTGTT",1))
print(bioalgorithms.reverse_complement("AAAAAGCATAAACATTAAAGAG"))
print(bioalgorithms.frequent_words_mismatch("ACGTTGCATGTCGCATGATGCATGAGAGCT",4,1))
print(bioalgorithms.approximate_pattern_matching("AAAAAGCATAAACATTAAAGAG","AAAAA",0))
print(bioalgorithms.approximate_pattern_count("AAAAAGCATAAACATTAAAGAG","AAAAA",0))
print(bioalgorithms.min_skew("CATGGGCATCGGCCATACGCC"))
print(bioalgorithms.clump_finding("CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAG",5,50,4))
print(bioalgorithms.pattern_count("cgatatatccatag","ata"))
print(bioalgorithms.frequent_words("actgactcccaccccc",3))
print(bioalgorithms.pattern_count_positions("cgatatatccatag","ata"))
print(bioalgorithms.hamming_distances("cgatatatccatag","ata"))
"""