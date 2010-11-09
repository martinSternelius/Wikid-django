# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from WikId.wiki.models import Article, Article_section, get_query
from django.http import HttpResponse
from django.template import Context, loader, RequestContext


def index(request):

    articles = Article.objects.all().order_by('-pub_date')[:5]
    start_article = Article.objects.get(title="Start Artikel")
    start_article.get_sections()
	users = User.objects.all()	
    
    for section in start_article.sectionList:
        section.section_heading = parse(section.section_heading)
        section.section_text = parse(section.section_text)
    
    return render_to_response('index.html', {'articles': articles, 'users':users, 'start_article': start_article})


def view_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.get_sections()
    
    for section in article.sectionList:
        section.section_heading = parse(section.section_heading)
        section.section_text = parse(section.section_text)
        
    return render_to_response('view_article.html', {'article': article})
	
def register_user(request):
    
    user_data = request.POST
    
    if request.POST:
        user = User(user_name=user_data['user_name'], e_mail=user_data['e_mail'], password=user_data['password'])
		user.save()
        
    return render_to_response('register_user.html', {'user_data':user_data}, context_instance=RequestContext(request))
	
def insert_test_data(request):
    insert_pub_date = datetime.datetime.now()
    articles = [Article(title="Article1", pub_date = insert_pub_date), Article(title="Article2", pub_date = insert_pub_date), Article(title="Article3", pub_date = insert_pub_date)]
    
    i = 1
    for article in articles:
        article.save()
        article.article_section_set.create(section_text = "''kursiv'' '''fetstil'''", section_heading="==Rubrik" + str(i) + "==", order=1)
        article.article_section_set.create(section_text = "''kursiv'' '''fetstil'''", section_heading="===Underrubrik===", order=1)
        article.article_section_set.create(section_text = "''kursiv'' '''fetstil'''", section_heading="===Underrubrik2===", order=2)
        article.article_section_set.create(section_text = "''kursiv'' '''fetstil'''", section_heading="==Rubrik" + str(i) + "==", order=2)
        article.article_section_set.create(section_text = "''kursiv'' '''fetstil''' En lista: *sak1 *sak2 *sak3", section_heading="===Underrubrik===", order=1)
        article.article_section_set.create(section_text = "''kursiv'' '''fetstil'''", section_heading="===Underrubrik2===", order=2)
        i+=1
		
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        article_query = get_query(query_string, ['title', 'article_section__section_text', 'article_section__section_heading'])
        
        articles = Article.objects.filter(article_query).order_by('-pub_date')
        
    return render_to_response('article_list.html',
                          { 'query_string': query_string, 'articles': articles},
                          context_instance=RequestContext(request))

