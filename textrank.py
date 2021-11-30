import networkx as nx
from itertools import chain
from collections import Counter

def scan_vocabulary(sentences, min_count=1, stop_words=set()):
  
    word_lst = (s.split(" ") for s in sentences)
    word_lst = ([w for w in w_l if w not in stop_words] for w_l in word_lst)
    word_counter = Counter(chain.from_iterable(word_lst))
    word_counter = {w: c for w, c in word_counter.items() if c >= min_count}
    # idx_to_vocab: count가 높을 수록 앞에 등장
    idx_to_vocab = [w for w, c in sorted(
        word_counter.items(), key=lambda x: -x[1])]
    vocab_to_idx = {w: idx for idx, w in enumerate(idx_to_vocab)}
    return idx_to_vocab, vocab_to_idx

def vocab_cooccurrence(sentences, vocab_to_idx, window=3, min_cooccurrence=1):
    """
    - window의 길이를 고려하여, 한 문장 내 cooccurrence를 고려하여 리턴. 
    - 한 방향으로만 리턴.
    """
    cooccurrence_dict = {}
    for s in sentences:
        tokens = [t.strip() for t in s.split(" ")]
        # vocab에 있는 것들만 남김.
        tokens = [vocab_to_idx[t] for t in tokens if t in vocab_to_idx]
        for i, token1 in enumerate(tokens):
            left_lim_idx = max(0, i-window)
            right_lim_idx = min(len(tokens), i+window)
            for token2 in tokens[left_lim_idx:right_lim_idx]:
                if token1 != token2:
                    key = tuple(sorted([token1, token2]))
                    if key in cooccurrence_dict:
                        cooccurrence_dict[key] += 1
                    else:
                        cooccurrence_dict[key] = 1
    return {k: v for k, v in cooccurrence_dict.items() if v >= min_cooccurrence}

def word_graph(sentences, min_count=1, min_cooccurrence=1, window=3, stop_words=set()):
    """
    - scan_vocabulary를 사용해서, min_count를 넘기고, stop_word에 속하지 않는 vocab만 남기고 
    - vocab_cooccurrence에서 window를 고려하여, vocab간의 edge들을 모두 가져오고
    - 이를 Graph로 만들어서 리턴.
    """
    idx_to_vocab, vocab_to_idx = scan_vocabulary(
        sentences, min_count=min_count, stop_words=stop_words)
    coor_dict = vocab_cooccurrence(
        sentences, vocab_to_idx, window=window, min_cooccurrence=min_cooccurrence)
    G = nx.Graph()
    for i, node_name in enumerate(idx_to_vocab):
        G.add_node(i, name=node_name)
    for (n1, n2), coor in coor_dict.items():
        G.add_edge(n1, n2, coor_count=coor)
    return G




#nx.pagerank(G, weight='coor_count')