# Name: Konstantinos Vardakas 
# AM: 522

def read_file(filename):
    '''
    Διαβάζει το αρχείο filename (transactions.txt ή queries.txt) 
    και γυρνάει μία λίστα από sets (όχι duplicates)    
    '''
    with open(filename, "r") as f:
        outlist = [line.strip()[1: -1].split(',') for line in f]
    outlist = [set([int(entry) for entry in line]) for line in outlist]
    return outlist

def naive_method(query, transactions):
    '''
    Μέθοδος αναφοράς naive method, που επιστρέφει τα transactions που εμπεριέχουν όλα
    τα αντικείμενο του query, με την μέθοδο των set, issubset().
    '''
    ids = [i for i, transaction in enumerate(transactions) if query.issubset(transaction)]
    return ids

def bitmap(line):
    '''
    Δημιουργία bit map για μία γραμμή είτε του transaction είτε του queries
    Το bit που δημιουργείται αρχίκοποιείται με την τιμή μηδέν
    και τοποθετείται ένα στις θέσεις του κάθε αντικειμένου που βρίσκεται στο line
    μετρώντας από δεξιά, δηλαδή από το least significant bit με τον bit operator << 
    '''
    bitmap_value = 0
    for item in line:
        # Βάλε 1 αριστερά στη θέση του item (1<<item)
        # Παράλληλα κράτα κάθε ένα που έχει μπει πιο πριν με το bitwise or
        bitmap_value |= (1 << item)
        
    return bitmap_value

def to_sigfile(transactions):
    '''
    Συνάρτηση για δημιουργία sigfile, περνώντας κάθε transaction
    του transactions από την προηγούμενη συνάρτηση bitmap
    '''
    return list(map(bitmap, transactions))

def save_file(list_to_save, save_name):
    '''
    Συνάρτηση αποθήκευσης των αποτελεσμάτων
    χρησιμοποιείται για αποθήκευση το sigfile
    '''
    with open(save_name, 'w') as f:
        for line in list_to_save:
            f.write(f"{str(line)}\n")

            
def signature_file(query, transactions):
    '''
    Συνάρτηση για query βαση των signature file
    Για δεδομένο query, συγκρίνεται το tsansaction με το query
    με το λογικό and, και αν τα bits είναι ίδια με το αρχικό query, 
    προστίθεται στην λιστα των ids
    '''
    ids = [i for i, t in enumerate(transactions) if query&t == query]
    return ids


def bitslice(transactions):
    '''
    Συνάρτηση που δημιουργεί το bitslice signature file για τα transactions
    Αρχικοποιείται μία λίστα με μηδενικά bits για κάθε αντικείμενο και
    τοποθετείται σε κάθε αντικείμενο η τιμή 1, στη θέση του id transaction
    που βρέθηκε το αντικείμενο, αρχίζοντας από το least significant bit, 
    όμοια με τη συνάρτηση bitmap
    '''
    max_item = max(max(t) for t in transactions)
    out = [0] * (max_item + 1)
    for i, transaction in enumerate(transactions):
        for t in transaction:
            out[t] |= (1 << i)
    return out
    

def bitsliced_signature_file(query, bitslice_trans):
    '''
    Συνάρτηση query για την λίστα bitslice που παρήχθησε από την 
    προηγούμενη συνάρτηση
    Για κάθε αντικείμενο του query γίνεται σύγκριση bitwise and 
    και μετά την σύγκριση απομένουν τα transactions όπου υπήρχαν
    όλα τα αντικείμενα του query.
    Για την κατασκευή των ids, ελέγχονται οι θέσεις όπου περιέχεται
    μονάδα (transaction με όλα τα αντικείμενα) και προστίθεται στα ids
    '''
    items = list(query)

    # Αρχίζοντας από το bitmap του πρώτου αντικειμένου
    result = bitslice_trans[items[0]]

    # Bitwise AND με όλα τα υπόλοιπα αντικείμενα
    # μηδενίζονται όσα transactions δεν υπάρχουν στα δύο που συγκρίνονται
    for item in items[1:]:
        result &= bitslice_trans[item]
    
    # στις θέσεις που έχει απομείνει 1,
    # κρατάω το id του transaction
    ids = []
    for i in range(result.bit_length()):
        if (result >> i) & 1:
            ids.append(i)

    return ids

def save_enu_file(list_to_save, save_name):
    '''
    Συνάρτηση αποθήκευσης των αποτελεσμάτων με id (enumerate)
    χρησιμοποιείται για αποθήκευση του bitslice
    '''
    with open(save_name, 'w') as f:
        for i, line in enumerate(list_to_save):
            f.write(f"{i}: {str(line)}\n")
            
def build_inverted_file(transactions):
    '''
    Συνάρτηση για δημιουργία του inverted file των transactions, με key το αντικείμενο
    και val μια λίστα με τα transactions στα οποία υπάρχει αυτό το αντικείμενο
    '''
    
    inverted = {}
    for i, transaction in enumerate(transactions):
        for item in transaction:
            if item not in inverted:
                inverted[item] = []
            inverted[item].append(i)

    return inverted


def merge_intersection(lists):
    '''
    Υπολογίζει την τομή πολλών ταξινομημένων λιστών με χρήση merge αλγορίθμου για sorted lists
    Ξεκινά από την πρώτη λίστα και συγκρίνει ταυτόχρονα τα στοιχεία με κάθε επόμενη λίστα
    και διατηρεί μόνο τα κοινά στοιχεία σε μία νέα λίστα αποτελεσμάτων
    Επιστρέφει τη λίστα με τα κοινά ids συναλλαγών.
    '''
    if not lists:
        return []

    result = lists[0]
    for lst in lists[1:]:
        i = j = 0
        new_result = []
        while i < len(result) and j < len(lst):
            if result[i] == lst[j]:
                new_result.append(result[i])
                i += 1
                j += 1
            elif result[i] < lst[j]:
                i += 1
            else:
                j += 1
        result = new_result
        if not result: # Early stopping εάν τα δύο αντικείμενα που συγκρίνονται δεν βρίσκονται σε κάποιο transaction
            break
    return result


def inverted_file(query, inverted_index):
    '''
    Δημιουργείται η λίστα με τα transaction id των αντικειμένων 
    και δίνεται στην merge intesection για να βρεθούν τα transactions
    του query
    '''
    lists = []
    for item in query:
        lists.append(inverted_index[item])

    return merge_intersection(lists)
    

def save_inverted_file(inverted_index, filename):
    '''
    Αποθήκευση του inverted file ταξινομημένου ως προς τα keys
    '''
    with open(filename, 'w') as f:
        for item in sorted(inverted_index):
            f.write(f"{item}: {inverted_index[item]}\n")
            