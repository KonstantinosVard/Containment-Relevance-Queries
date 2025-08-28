# Name: Konstantinos Vardakas 
# AM: 522

import sys
import time
from relevance_functions import *

def time_method(method, query, transactions, idf, k, qnum):
    """
    Χρονομετρεί την εκτέλεση της συνάρτησης και μορφοποιεί την εκτύπωση της εξόδου
    """
    function_name = ' '.join(method.__name__.split('_'))
    start = time.perf_counter()
    results = list(map(lambda q: method(q, transactions, idf, k), query))
    end = time.perf_counter()
    if qnum != -1:  # εκτύπωση αποτελεσμάτων αν είναι συγκεκριμένο query
        print(f"{function_name} result:")
        print(results[0])
    print(f"{function_name} computation time = {end - start:.6f} sec")

def main(transactions_path, queries_path, qnum, method, k):
    # Διάβασμα των input
    transactions = read_file(transactions_path)
    queries = read_file(queries_path)

    # Δημιουργία inverted file και δομής idf
    inverted_index, idf = build_inverted_file_occ(transactions)
    save_inverted_file_occ(inverted_index, idf, 'invfileocc.txt')

    # Επιλογή των query
    if qnum == -1:
        query = queries[:]  # όλα τα queries
    elif 0 <= qnum < len(queries):
        query = [queries[qnum]]  # συγκεκριμένο query
    else:
        print("Invalid qnum")
        sys.exit(1)

    # Εκτέλεση μεθόδου
    if method == -1:
        time_method(naive_relevance_query, query, transactions, idf, k, qnum)
        time_method(inverted_file_method, query, inverted_index, idf, k, qnum)
    elif method == 0:
        time_method(naive_relevance_query, query, transactions, idf, k, qnum)
    elif method == 1:
        time_method(inverted_file_method, query, inverted_index, idf, k, qnum)
    else:
        print("Invalid method")
        sys.exit(1)

if __name__ == "__main__":
    args_original = sys.argv[1:]

    if len(args_original) != 5:
        print("Usage: python relevance_main.py <transactions_path> <queries_path> <qnum> <method> <k>")
        sys.exit(1)

    args = [arg if arg.endswith('.txt') else arg + '.txt' for arg in args_original[:2]]
    args.extend([int(arg) for arg in args_original[2:]])
    main(*args)