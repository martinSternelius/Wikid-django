from django.db import models
import datetime
from django.contrib import admin
import re
from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
            
        return query



class Article (models.Model):
    title = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.title
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    
    def get_sections (self):
        self.sectionList = self.article_section_set.all()
        
    def Order_sectionList(self, sectionList):
        
       return self.sectionList
    
class Article_section (models.Model):
   
    article = models.ForeignKey(Article)
    order = models.IntegerField(max_length = 1, null = True)
    parent_section = models.ForeignKey("self", related_name = "parent", null = True, blank=True)
    
    section_text = models.TextField()
    section_heading = models.CharField(max_length = 200, null = True, blank=True)    

class User (models.Model):
    
    user_name = models.CharField(max_length = 200)
    e_mail = models.CharField(max_length = 200, null=True)
    password = models.CharField(max_length=200)