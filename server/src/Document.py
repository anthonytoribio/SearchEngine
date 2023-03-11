class Document:
    def __init__(self, index,tf_dict, url:str, hrefs, title: str, desc: str, length: int):
        self.docid = index
        self.doc_tf_dict = tf_dict
        self.docUrl = url
        self.title = title
        self.desc = desc
        self.length = length
        self.pagerank = 1.0
        self.parents =[]
        #children stands for the valid outgoing urls
        self.children = []
        self.out_urls = hrefs
        
        
    def update_pagerank(self, randomness, document_length, docDict):
        in_neighbors = self.parents
        running_sum = 0
        for n in in_neighbors:
            n_page = docDict[n].pagerank
            nChildLen = len(docDict[n].children)
            if nChildLen == 0:
                nChildLen = 1
            running_sum += n_page / nChildLen

        if len(in_neighbors) == 0:
            self.pagerank = 0
            return

        random_walk = randomness / document_length
        self.pagerank = random_walk + (1-randomness) * running_sum