class Document:
    def __init__(self, index,tf_dict, url:str):
        self.docid = index
        self.doc_tf_dict = tf_dict
        self.docUrl = url