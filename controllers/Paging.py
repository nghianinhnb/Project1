from math import ceil

class Paging:
    def __init__(self, list, len_each_page=1, page=1):
        self.pos = page;
        self.size = ceil(len(list)/len_each_page)
        if page>self.size:  self.page = None

        page = page - 1
        if len_each_page*(page+1)>len(list):
            self.page = list[len_each_page*page : ]
        else:
            self.page = list[len_each_page*page : len_each_page*(page+1)]