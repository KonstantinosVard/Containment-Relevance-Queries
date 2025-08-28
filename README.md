# Containment and Relevance Queries Project

### MSc Data Science & Engineering · Complex Data Management Course · Project 3/4: Containment and Relevance Queries

## Overview

This project implements and evaluates multiple methodologies for processing containment and relevance queries on transactional data. It features four different containment query methods and two relevance query approaches with efficient processing techniques using bitmap operations, inverted files, and optimized algorithms.

## File Structure

### Data Files:
- `transactions.txt` - Contains transaction data with item sets
- `queries.txt` - Contains containment/relevance queries to be evaluated
- `sigfile.txt` - Generated signature file (after program execution)
- `bitslice.txt` - Generated bitslice signature file (after program execution)
- `invfile.txt` - Generated inverted file for containment queries (after program execution)
- `invfileocc.txt` - Generated inverted file with occurrences for relevance queries (after program execution)

### Source Code Files:

#### Containment Queries:
- `containment_functions.py` - Helper functions for containment query methods
- `containment_main.py` - Main program for executing containment queries

#### Relevance Queries:
- `relevance_functions.py` - Helper functions for relevance query methods
- `relevance_main.py` - Main program for executing relevance queries

## Installation & Execution

### Prerequisites:
- Python 3.x
- No external dependencies required

### Execution Instructions:

1. **Place all files in the same directory**
2. **Open terminal in the project directory**

#### Run Containment Queries:
```bash
python containment_main.py <transactions_file> <queries_file> <qnum> <method>
```
- `transactions_file`: File containing transaction data (default: transactions.txt)
- `queries_file`: File containing queries (default: queries.txt)
- `qnum`: Specific query number to execute, or 'all' for all queries
- `method`: Query method to use: 'naive', 'sigfile', 'bitslice', or 'invfile'

Example: `python containment_main.py transactions.txt queries.txt all invfile`

#### Run Relevance Queries:
```bash
python relevance_main.py <transactions_file> <queries_file> <qnum> <method> <k>
```
- `transactions_file`: File containing transaction data (default: transactions.txt)
- `queries_file`: File containing queries (default: queries.txt)
- `qnum`: Specific query number to execute, or 'all' for all queries
- `method`: Query method to use: 'naive' or 'invfile'
- `k`: Number of top results to return

Example: `python relevance_main.py transactions.txt queries.txt 2 invfile 10`

**Note:** File extensions (.txt) are optional in command arguments.

## Implementation Details

### Containment Query Methods:

1. **Naive Method**: Simple reference implementation checking subset relationships
2. **Signature File**: Uses bitmap operations with bitwise AND for efficient containment checks
3. **Bitslice Signature File**: Creates object-based bitvectors and performs logical AND operations
4. **Inverted File**: Uses sorted transaction lists and merge intersection algorithm

### Relevance Query Methods:

1. **Naive Method**: Calculates relevance scores by examining each transaction individually
2. **Inverted File Method**: Uses precomputed occurrence counts and IDF values for efficient scoring

### Key Features:
- Bitmap operations using bitwise operators for efficient containment checking
- Merge algorithms for sorted list intersections and unions
- IDF (Inverse Document Frequency) calculation for measuring item rarity
- Relevance scoring using occurrence counts and IDF values
- Efficient processing of both single and multiple queries

## Output

- **Generated Files**: Signature files, bitslice structures, and inverted files with/without occurrences
- **Query Results**: Returns transaction IDs that satisfy containment conditions or top-k most relevant transactions
- **Performance Timing**: Measures execution time for each query method

## Performance Considerations

- Signature file methods use bitmap operations for fast containment checks
- Inverted file methods utilize sorted lists and merge algorithms for efficient intersections
- Relevance queries incorporate both frequency and rarity factors in scoring
- All methods are optimized to avoid unnecessary computations

## Notes

- The implementation handles both set semantics (containment) and bag semantics (relevance)
- Bitmap operations use integer bitvectors with bits numbered from right to left (LSB to MSB)
- Inverted files store sorted transaction lists for efficient merge operations
- Relevance scoring uses the formula: rel(τ, q) = Σ(i∈q) occ(i, τ) × idf(i)

## Author

**Konstantinos Vardakas**  

---

*This project demonstrates efficient implementation of containment and relevance query processing using various indexing techniques and optimization strategies for transactional data analysis.*
