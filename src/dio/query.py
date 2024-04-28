class Query:
    id = ""
    http_request = ""
    odata_query_name = ""
    query = ""
    title = ""
    
    def __init__(self, id , http_request, odata_query_name , query, title):       
        self.id = id
        self.http_request = http_request
        self.odata_query_name = odata_query_name
        self.query = query
        self.title  = title
        
    def PrintId(self):
        print(self.id)