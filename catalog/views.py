from django.shortcuts import render
from django.views import generic
from catalog.models import (
	Book, 
	Author, 
	BookInstance,
	Genre,
	Language,
)
from django.db.models import Q


# Create your views here.

def index(request):
	""" View function for home page of site. """

	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# available books ( status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# the 'all()' is implied by default.
	num_authors = Author.objects.count()

	# counts of genres
	num_genres = Genre.objects.all().count()

	# counts of languages
	num_languages = Language.objects.all().count()

	# counts of book containing 'vapu' in title
	num_vapu = Author.objects.filter(first_name__contains='वपु').count()
	
	# number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1


	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_languages': num_languages,
		'num_genres': num_genres,
		'num_vapu': num_vapu,
		'num_visits': num_visits,
	}

	query = ''
	if request.GET:
		query = request.GET['q']
		context['query'] = str(query)
		#submitbutton = request.GET.get('submit')


	books = get_book_queryset(query)
	context['books'] = books
	#context['submit'] = submitbutton
	# render the HTML template index.html with the data in the context variable
	return render(request, 'catalog/index.html', context=context)

class BookListView(generic.ListView):
	model = Book
	ordering = ['title']
	paginate_by = 5

class BookDetailView(generic.DetailView):
	model = Book

class AuthorListView(generic.ListView):
	model = Author
	ordering = ['last_name']

class AuthorDetailView(generic.DetailView):
	model = Author

class GenreListView(generic.ListView):
	model = Genre
	ordering = ['name']

class GenreBookListView(generic.ListView):
	model = Book
	template_name = 'catalog/genre_book_list.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'genrebooks'
    
	def get_queryset(self):
	     
	 	# filter by a variable captured from url, for example
		return Book.objects.filter(genre=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
	
		context = super(GenreBookListView, self).get_context_data(**kwargs)
		context['genre'] = Genre.objects.get(pk=self.kwargs['pk'])
  
		return context


class LanguageListView(generic.ListView):
	model = Language
	ordering = ['name']

class LanguageBookListView(generic.ListView):
	model = Book
	template_name = 'catalog/language_book_list.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'languagebooks'
    
	def get_queryset(self):
	     
	 	# filter by a variable captured from url, for example
		return Book.objects.filter(language=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
	
		context = super(LanguageBookListView, self).get_context_data(**kwargs)
		context['language'] = Language.objects.get(pk=self.kwargs['pk'])
  
		return context

def get_book_queryset(query=None):
	queryset = []
	queries = query.split(' ') # python install 2019 = ['python', 'install', '2019']
	for q in queries:
		author = Author.objects.filter()
		books = Book.objects.filter(
				Q(title__icontains= q) |
				Q(summary__icontains=q)
			).distinct()

		for book in books:
			queryset.append(book)

	return list(set(queryset))



'''
def search(request):        
    if request.method == 'GET': # this will be GET now      
        book_name =  request.GET.get('search') # do some research what it does       
        try:
            status = Book.objects.filter(title__icontains=book_name) 
        return render(request, "search.html", {"books":status} )
    else:
        return render(request,"search.html",{})
'''        