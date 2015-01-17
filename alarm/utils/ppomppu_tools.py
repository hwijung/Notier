import re
import urllib2

from bs4 import BeautifulSoup

class PpomppuParsor():
    class ClassNames:
        FOREIGN_PPOMPPU_TITLE_0 = 'list0'
        FOREIGN_PPOMPPU_TITLE_1 = 'list1'
        
        FOREIGN_PPOMPPU_TITLE_CLASS_ENABLED = 'list_title'
        FOREIGN_PPOMPPU_TITLE_COLOR_DISABLED = '#ACACAC'
        
    class Urls:
        FOREIGN_PPOMPPU = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu4'
            
    def get_foreign_ppomppu_titles(self):
        entries = []
        
        response = urllib2.urlopen(self.Urls.FOREIGN_PPOMPPU)
        html = response.read().decode("cp949", "ignore").encode("utf-8", "ignore")
        
        bs = BeautifulSoup(html)
        titles_tags = ( bs.findAll('tr', { 'class': self.ClassNames.FOREIGN_PPOMPPU_TITLE_0 } ) 
                   + bs.findAll('tr', { 'class': self.ClassNames.FOREIGN_PPOMPPU_TITLE_1 }) )
        
        for title in titles_tags:
        
            # [0] Index, [1] Category, [2] Author, [3] Subject & Comments, 
            # [4] Time, [5] Recommend, [6] View
            attributes = title.find_all('td', recursive = False )
                    
            # [0] Index
            index = attributes[0].string
            
            # [1] Category
            category = attributes[1].nobr.string
            
            # [2] Author
            author = attributes[2].find('span', { 'class': 'list_name' } ).string
            
            # [3] Subject & Comments
            subject_tag = attributes[3].find('font', { 'class': self.ClassNames.FOREIGN_PPOMPPU_TITLE_CLASS_ENABLED } )
            active = True
                 
            if subject_tag == None:
                subject_tag = attributes[3].find('font', { 'color': self.ClassNames.FOREIGN_PPOMPPU_TITLE_COLOR_DISABLED } )
                active = False
            
            subject = subject_tag.string
            link = subject_tag.parent['href']
            
            if subject_tag.parent.parent.find('span', {'class':'list_comment2'}) == None:
                comment_number = 0
            else:
                comment_number = int(subject_tag.parent.parent.find('span', {'class':'list_comment2'}).span.string)
            
            # [4] Time
            time = attributes[4].nobr.string
            
            # [5] Recommend
            recommend = attributes[5].string
            
            # [6] View
            view = int(attributes[6].string)
            
            entries.append ( { 'index': index, 'category': category, 'author': author, 
                              'subject': subject, 'link': link, 'comment_number': comment_number,
                              'time': time, 'recommend': recommend, 'view': view, 'active': active } )

        return entries
    
            
            
            
            
                        
        
        