# Name: Konstantinos Vardakas 
# AM: 522

def read_file(filename):
    """
    Διαβάζει το αρχείο filename (transactions.txt) 
    και γυρνάει μία λίστα από λίστες   
    """
    with open(filename, "r") as f:
        outlist = [line.strip()[1:-1].split(',') for line in f]
    outlist = [[int(entry) for entry in line if entry.strip()] for line in outlist]
    return outlist

def build_inverted_file_occ(transactions):
    """
    Δημιουργεί δύο λεξικά:
    inverted_index, όπου για κάθε αντικείμενο, καταγράφει λίστα με [transaction_id, occ]
    trf, με το |T|/trf(i,T) για κάθε αντικείμενο
    """
    N = len(transactions)
    inverted_index = {}   # item -> list of [transaction_id, occ]
    trf = {}              # item -> σε πόσα διαφορετικά transactions εμφανίζεται

    for tid, transaction in enumerate(transactions): # Για κάθε συναλλαγή
        # καταμέτρηση της συχνότητας των αντικειμένων
        # στο συγκεκριμένο transaction
        occ_dict = {} 
        
        for item in transaction:
            if item not in occ_dict:
                occ_dict[item] = 0
            occ_dict[item] += 1

        # Για κάθε αντικείμενο και συχνότητα του transaction
        # Δημιουργία του item : [id, occ]
        for item, occ in occ_dict.items():
            if item not in inverted_index:
                inverted_index[item] = []
            inverted_index[item].append([tid, occ])

            # Για κάθε item του transaction +1,
            # ώστε να μετρηθεί σε πόσα διαφορετικά
            # transaction υπάρχει το item
            if item not in trf:
                trf[item] = 0
            trf[item] += 1 

    idf = {item: N / trf[item] for item in trf}
    return inverted_index, idf

def merge_union(lists):
    """
    Υπολογίζει την ένωση ταξινομημένων λιστών της μορφής [tid, occ] 
    χρησιμοποιώντας αλγόριθμο συγχώνευσης (merge).
    
    Επιστρέφει μια λίστα από μοναδικά ζεύγη [tid, occ_list], 
    όπου occ_list περιέχει τις συχνότητες εμφάνισης (occ) του tid για κάθε αντικείμενο.
    Αν το αντικείμενο δεν εμφανίζεται σε ένα συγκεκριμένο tid, καταχωρείται ως 0.
    """
    result = []  # Λίστα για την αποθήκευση των αποτελεσμάτων
    pointers = [0] * len(lists) # Ένας δείκτης για κάθε λίστα, δείχνει σε ποιο στοιχείο είμαστε
    
    # Συνεχίζουμε όσο υπάρχουν στοιχεία σε τουλάχιστον μία λίστα
    while True:
        # Έλεγχος αν υπάρχουν διαθέσιμα στοιχεία σε κάποια λίστα
        has_elements = False
        for i in range(len(lists)):
            if pointers[i] < len(lists[i]):
                has_elements = True
                break
        if not has_elements:
            break  # Τερματισμός αν δεν υπάρχουν άλλα στοιχεία

        # Εύρεση του μικρότερου tid από τα τρέχοντα στοιχεία όλων των λιστών
        min_tid = float('inf')
        for i in range(len(lists)):
            if pointers[i] < len(lists[i]) and lists[i][pointers[i]][0] < min_tid:
                min_tid = lists[i][pointers[i]][0]

        # Αν δεν βρέθηκε έγκυρο tid, τερματισμός
        if min_tid == float('inf'):
            break

        # Συλλογή των συχνοτήτων (occ) για το min_tid από κάθε λίστα
        occ_list = []
        for i in range(len(lists)):
            if pointers[i] < len(lists[i]) and lists[i][pointers[i]][0] == min_tid:
                occ_list.append(lists[i][pointers[i]][1])  # Προσθήκη συχνότητας
                pointers[i] += 1  # Μετακίνηση του δείκτη στην επόμενη θέση
            else:
                occ_list.append(0)  # Το αντικείμενο δεν υπάρχει σε αυτό το tid

        # Προσθήκη του tid και της λίστας συχνοτήτων στο αποτέλεσμα
        result.append([min_tid, occ_list])

    return result


def inverted_file_method(query, inverted_index, idf, k):
    """
    Εκτελεί αποτίμηση σχετικότητας για ένα query με βάση τις συναλλαγές που περιέχουν τα αντικείμενά του.
    Επιστρέφει τις top-k συναλλαγές με το μεγαλύτερο relevance score rel(t, q).
    """
    # Εξαγωγή των λιστών [tid, occ] για κάθε αντικείμενο του query
    lists = []
    query_items = set(query)  # Αφαίρεση duplicates
    query_items_list = list(query_items)  # Λίστα για διατήρηση σταθερής σειράς στα αντικείμενα
    for item in query_items:
        if item in inverted_index:
            lists.append(inverted_index[item])

    # Υπολογισμός της ένωσης των συναλλαγών που περιέχουν τουλάχιστον ένα αντικείμενο του query
    union = merge_union(lists)

    # Υπολογισμός του rel(t, q) για κάθε συναλλαγή
    results = []
    for tid, occ_list in union:
        rel = 0.0
        # Για κάθε αντικείμενο του query, προσθέτουμε τη συμβολή του στη συνάρτηση σχετικότητας
        for occ, item in zip(occ_list, query_items_list):
            if occ > 0 and item in idf:
                rel += occ * idf[item]  # rel += occ(i, τ) * (|T| / trf(i,T))
        
        if rel > 0:
            results.append([rel, tid])  # Κρατάμε μόνο όσες έχουν σχετικότητα

    # Ταξινόμηση των αποτελεσμάτων κατά φθίνουσα σχετικότητα και επιλογή των top-k
    results.sort(reverse=True)
        
    return results[:min(k, len(results))]
    
def naive_relevance_query(query, transactions, idf, k=10):
    """
    Υπολογίζει rel(t, q) διατρέχοντας όλες τις συναλλαγές.
    """
    # Λεξικό για την αποθήκευση των rel για κάθε συναλλαγή
    relevance_scores = {}
    
    # Καταμέτρηση εμφανίσεων αντικειμένων στη συναλλαγή 
    # ομοια με την συνάρτηση build_inverted_file_occ
    for tid, transaction in enumerate(transactions):
        occ_dict = {}
        for item in transaction:
            if item not in occ_dict:
                occ_dict[item] = 0
            occ_dict[item] += 1

        # υπολογισμός rel για την συναλλαγή 
        rel = 0
        for item in query:
            if item in occ_dict and item in idf:
                rel += occ_dict[item] * idf[item]
        if rel > 0:
            relevance_scores[tid] = rel
            
    # Επιστροφ΄ή των αποτελεσμάτων sorted και ως [rel, tid]
    results = sorted([[rel, tid] for tid, rel in relevance_scores.items()], key=lambda x: x[0], reverse=True)
        
    return results[:min(k, len(results))]
    
def save_inverted_file_occ(inverted_index, idf, filename="invfileocc.txt"):
    '''
    Συνάρτηση αποθήκευσης των αποτελεσμάτων
    χρησιμοποιείται για αποθήκευση του invfileocc
    sorted ως προς τα keys
    '''
    with open(filename, 'w') as f:
        for item in sorted(inverted_index.keys()):
            idf_value = idf[item]
            entry = inverted_index[item]
            f.write(f"{item}: {idf_value}, {entry}\n")
    