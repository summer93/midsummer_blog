class PageInfo(object):
    def __init__(self,current_Pag,all_count,per_page,url_content,show_page=11):
        try:
            self.current_Page = int(current_Pag)
        except Exception as e:
            self.current_Page = 1
        self.all_count = all_count
        self.per_page = per_page
        self.url_content = url_content

        a,b = divmod(all_count,per_page)
        if b:
            a = a + 1
        self.all_pager = a
        self.show_page = show_page

    @property
    def start(self):
        return (self.current_Page - 1) * self.per_page

    @property
    def end(self):
        return self.current_Page * self.per_page

    @property
    def pager(self):
        page_list = []

        half = int((self.show_page-1)/2)
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager
        else:
            if self.current_Page <= half:
                begin = 1
                stop = self.show_page
            else:
                if self.current_Page + half > self.all_pager:
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager
                else:
                    begin = self.current_Page - half
                    stop = self.current_Page + half
        if self.current_Page <= 1:
            prev = "<a  href='%s?page=1'>上一页</a>"%self.url_content
        else:
            prev = "<a  href='%s?page=%s'>上一页</a>"%(self.url_content,self.current_Page-1,)
        page_list.append(prev)

        for i in range(begin,stop+1):
            if i == self.current_Page:
                temp = "<a style='color:red' href='%s?page=%s'>%s</a>"%(self.url_content,i,i,)
            else:
                temp = "<a  href='%s?page=%s'>%s</a>"%(self.url_content,i,i,)
            page_list.append(temp)

        if self.current_Page >= self.all_pager:
            nex = "<a href='%s?page=%s'>下一页</a>"%(self.url_content,self.all_pager,)
        else:
            nex = "<a href='%s?page=%s'>下一页</a>" % (self.url_content,self.current_Page + 1,)
        page_list.append(nex)
        return ''.join(page_list)

