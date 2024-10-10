# CS613-NLP

## File Structure

1. Directory `<SourceName>-<TeamMemberName>` should contain `LinkScrape` directory where the Link scraping codes are present and `WebCrawl` directory where the Text Parsing from each weblink codes are present.
2. Additionally the main directory `<SourceName>-<TeamMemberName>` can contain the Jupyter Notebook where a dry run must have taken place before making the scraping and crawling links.
3. `badwords.json` contains the JSON file of Telugu + English bad words that are to be removed from the text.
4. `HuggingFace.ipynb` demonstrates how existing corpus in `.parquet` can be dowloaded.
5. Later these `.parquet` files have to be read using `pandas` and then have to be parsed for each row to get the text into separate `.txt` files.

### [Telugu Corpus Sheet](https://docs.google.com/spreadsheets/d/1Kr59i-8Gyhi3ehN_hLVCPdBcms7L07xNUUFsTW3uFDk/edit?gid=1042635267#gid=1042635267)


## MinHashLSH Algorithm

The MinHashLSH (MinHash Locality-Sensitive Hashing) algorithm is a powerful technique for estimating the Jaccard similarity between sets. The main idea is to reduce the dimensionality of the data while preserving the pairwise similarity between sets. The process involves several key steps:

### 1. Shingling
To begin with, a document is converted into a set of shingles (or k-grams). For instance, given a string, we can extract overlapping substrings of length $k$.

```math
S_k = \{ s_i, s_{i+1}, \ldots, s_{i+k-1} \}
```

where $s_i$ is the $i^{th}$ character in the string.

### 2. MinHashing
Next, a MinHash signature is generated for each set of shingles. This involves creating multiple hash functions $h_1, h_2, \ldots, h_n$ that map the shingles to a range of integers. The MinHash of a set $S$ is the minimum value produced by these hash functions.

The MinHash of set $S$ is defined as:

```math
\text{MinHash}(S) = \min_{s \in S} \{ h(s) \}
```

For  $k$ hash functions, we can generate a MinHash signature of length $k$:

```math
\text{signature}(S) = \begin{bmatrix}
\text{MinHash}_1(S) \\
\text{MinHash}_2(S) \\
\vdots \\
\text{MinHash}_k(S)
\end{bmatrix}
```

### MinHash: Estimating Jaccard Similarity
MinHash (short for Min-wise Independent Permutations Hashing) is a technique used to estimate the Jaccard similarity between two sets.

#### Jaccard Similarity
For two sets $A$ and $B$, the Jaccard similarity $J(A, B)$ is defined as:

```math
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
```

This measures the size of the intersection relative to the union of the sets. The closer the value is to 1, the more similar the sets are.

#### How MinHash Works
MinHash allows us to approximate the Jaccard similarity between two sets by applying a random permutation to the elements of each set and selecting the smallest (minimum) hash value of the elements after the permutation. By repeating this process with multiple hash functions (i.e., permutations), we can estimate the Jaccard similarity.

Let $h_1, h_2, \ldots, h_k$ be a family of random hash functions. For each set $A$, compute the minimum value of the hash functions for each permutation:

```math
\text{MinHash}(A) = \left( \min(h_1(A)), \min(h_2(A)), \ldots, \min(h_k(A)) \right)
```

The probability that the minimum hash values for two sets $A$ and $B$ are the same is equal to the Jaccard similarity:

```math
P(\min(h_i(A)) = \min(h_i(B)) ) = J(A, B)
```

Thus, the more MinHashes that match between two sets, the more similar the sets are, with the proportion of matching MinHashes approximating the Jaccard similarity:

```math
\hat{J}(A, B) \approx \frac{\text{Number of matching MinHashes}}{\text{Total number of MinHashes}}
```

#### MinHash in Practice
Instead of computing full hash permutations, practical implementations simulate random permutations using a fixed number of permutations (e.g., 128). The resulting signature is a compact representation of the set, allowing for fast comparison.

### Locality-Sensitive Hashing (LSH): Efficient Similarity Search
MinHashLSH builds on MinHash by enabling efficient approximate nearest-neighbor search. The goal of LSH is to quickly identify similar items in large datasets without comparing every possible pair.

#### Hash Buckets and LSH
LSH works by hashing similar items (sets or documents) into the same "bucket" with high probability, allowing us to efficiently retrieve candidate near-duplicates.

#### Key Idea
The MinHash signature for a set is divided into multiple "bands" of hash values. Each band is hashed into a separate hash table (bucket). If two items share the same band in at least one hash table, they are considered potential candidates for similarity (i.e., they are "near neighbors"). For example:

Let $s_1, s_2, \ldots, s_k$ be the MinHash signature for a document. Divide the signature into $b$ bands, each containing $r$ hash values (so that $k = b \times r$). Each band is hashed into a hash table:

```math
\text{BandHash}(i) = \text{hash}(s_{(i-1)r+1}, s_{(i-1)r+2}, \ldots, s_{ir})
```

The idea is that similar sets are more likely to share one or more band hash values, thus colliding in at least one hash table.

#### Probability of Collision
The probability that two documents $A$ and $B$ collide in at least one band is related to their Jaccard similarity. Let $p$ be the Jaccard similarity $J(A, B)$ between two sets. The probability that two sets do not collide in one band (i.e., they have different MinHash values in all $r$ positions of that band) is:

```math
P(\text{No collision in one band}) = (1 - p^r)
```

The probability that two sets do not collide in any of the $b$ bands is:

```math
P(\text{No collision in any band}) = (1 - p^r)^{b}
```

Therefore, the probability that two sets collide in at least one band is:

```math
P(\text{Collision}) = 1 - (1 - p^r)^{b}
```

This probability increases as the similarity $p$ increases, meaning that similar sets are likely to collide in at least one band, while dissimilar sets are unlikely to collide.

#### Tuning Parameters
1. $b$ (number of bands): More bands reduce false positives but increase false negatives.
2. $r$ (rows per band): More rows per band reduce false negatives but increase false positives.

#### False Positives and Negatives}
1. **False Positive**: Two dissimilar sets might collide in a bucket due to chance, causing them to be falsely flagged as similar.
2. **False Negative**: Two similar sets might not collide in any bucket, causing them to be missed.

LSH works by balancing these trade-offs, with parameters $b$ and $r$ controlling the precision of the approximation.

### Example Code
_Source: https://leons.im/posts/a-python-implementation-of-simhash-algorithm/_ <br>
_Souce: https://ekzhu.com/datasketch/minhash.html_
```python
import os
import re
from datasketch import MinHash, MinHashLSH

def get_features(s):
    """Extract 3-character shingles from the string."""
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

def get_minhash(content, num_perm=128):
    """Convert features derived from content to a MinHash object for LSH comparison."""
    minhash = MinHash(num_perm=num_perm)
    features = get_features(content)
    for feature in features:
        minhash.update(feature.encode('utf-8'))
    return minhash

def lsh_deduplication(documents, threshold=0.8, num_perm=128):
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    minhashes = {}

    # Create MinHash for each document and insert into LSH
    for doc_id, text in documents.items():
        minhash = get_minhash(text, num_perm=num_perm)
        minhashes[doc_id] = minhash

        lsh.insert(doc_id, minhash)

    # Deduplicate documents based on LSH
    deduplicated_docs = {}
    for doc_id in documents:
        similar_docs = lsh.query(minhashes[doc_id])
        if len(similar_docs) == 1:  # If only one match (itself), it's unique
            deduplicated_docs[doc_id] = documents[doc_id]

    return deduplicated_docs
```


### SQuAD Paper

[SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) <br>
[Paper Overview](https://sh-tsang.medium.com/brief-review-squad-100-000-questions-for-machine-comprehension-of-text-f191c6b670b8) <br>
[Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) <br>
[Dependency Parsing](https://towardsdatascience.com/natural-language-processing-dependency-parsing-cf094bbbe3f7) <br>
[Universal Dependency Table](https://universaldependencies.org/u/dep/) <br>
