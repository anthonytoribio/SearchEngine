class Document:
    def __init__(self, index,tf_dict, url:str, hrefs, title: str, desc: str):
        self.docid = index
        self.doc_tf_dict = tf_dict
        self.docUrl = url
        self.title = title
        self.desc = desc
        self.pagerank = 1.0
        self.parents =[]
        self.children = []
        self.out_urls = hrefs
        
        
    def update_pagerank(self, randomness, document_length):
        in_neighbors = self.parents
        pagerank_sum = sum((node.pagerank / len(node.children)) for node in in_neighbors)
        random_walk = randomness / document_length
        self.pagerank = random_walk + (1-randomness) * pagerank_sum