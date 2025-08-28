# Name: Konstantinos Vardakas 
# AM: 522

import sys
import time
from containment_functions import *

def time_method(method, queries, transactions, qnum):
    '''
    Χρονομετρεί την εκτέλεση της συνάρτησης και μορφοποιεί την εκτύπωση της εξόδου
    '''
    function_name = ' '.join(method.__name__.split('_'))
    start = time.perf_counter() # πιο ακριβές από time()
    results = list(map(lambda q: method(q, transactions), queries))
    end = time.perf_counter()
    if qnum != -1: # εκτύπωση αποτελεσμάτων αν είναι συγκεκριμένο query
        print(f"{function_name} result")
        print(set(results[0]))
    print(f"{function_name} computation time = {end - start:.6f} sec")


def main(transactions_path, queries_path, qnum, method):
    
    # Διάβασμα των transactions και queries
    transactions = read_file(transactions_path)
    queries =  read_file(queries_path)
    
    # Αποθήκευση του sigfile των transactions
    sigfile = to_sigfile(transactions)
    save_file(sigfile, 'sigfile.txt')

    # Αποθήκευση του bitslice transaction
    bit = bitslice(transactions)
    save_enu_file(bit, 'bitslice.txt')
    
    # Αποθήκευση του inverted file transaction
    inverted_index = build_inverted_file(transactions)
    save_inverted_file(inverted_index, 'invfile.txt')

    # Επιλογή των query
    # Εάν το query είναι συγκεκριμένο, μετατρέπεται σε λίστα,
    # γιατί στο time method τα αποτελέσματα εξάγονται με map() 
    if qnum == -1:
        query = queries[:]
    elif 0 <= qnum <= len(queries)-1:
        query = [queries[qnum]]
    else:
        print("Invalid qnum")
        sys.exit(1)

    # Επιλογή μεθόδου 
    if method == -1:
        query_bin =  to_sigfile(query)
        time_method(naive_method, query, transactions, qnum)
        time_method(signature_file, query_bin, sigfile, qnum)
        time_method(bitsliced_signature_file, query, bit, qnum)
        time_method(inverted_file, query, inverted_index, qnum)
        
    elif method == 0:
        time_method(naive_method, query, transactions, qnum)
    elif method == 1:
        query_bin = to_sigfile(query)
        time_method(signature_file, query_bin, sigfile, qnum)
    elif method == 2:
        time_method(bitsliced_signature_file, query, bit, qnum)
    elif method == 3:
        time_method(inverted_file, query, inverted_index, qnum)


if __name__ == "__main__":
    # Διάβασμα command line arguments
    args_original = sys.argv[1:]

    if len(args_original) != 4:
        print("Usage: python containment_main.py <transactions_path> <queries_path> <qnum> <method>")
        sys.exit(1)

    # Προσθήκη .txt αν δεν υπάρχει στο path, και μετατροπή των qnum και method σε int
    args = [arg if arg.endswith('.txt') else arg + '.txt' for arg in args_original[:2]]
    args.extend([int(arg) for arg in args_original[2:]])
    main(*args)
