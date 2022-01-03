from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic.base import View


from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    num_books_biography = Book.objects.filter(genre__name__icontains='Biography').count()

    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_books_biography': num_books_biography,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    #def get_queryset(self):
    #    return Book.objects.filter(title__icontains='Marie')[:5] # Get 5 books containing the title Marie

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        #context['some_data'] = 'This is just some data'
        #context['book_list'] = Book.objects.all()
        return context


class BookDetailView(generic.DetailView):
    model = Book

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        #context['author_list'] = Author.objects.all()
        return context

class AuthorDetailView(generic.DetailView):
    model = Author

def author_detail_view(request, primary_key):
    author = get_object_or_404(Author, pk=primary_key)
    return render(request, 'catalog/author_detail.html', context={'author': author})


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

'''
#class MyView(LoginRequiredMixin, View):
class MyView(PermissionRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!


@login_required()
@permission_required('catalog.can_mark_returned', raise_exception=True )
#@permission_required('catalog.can_edit')
def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
'''

from django.contrib.auth.mixins import LoginRequiredMixin

class LoandBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    login_url = '/accounts/login/'
    # login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

'''
class LibrarianView(PermissionRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    #permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!


@permission_required('catalog.can_mark_returned', raise_exception=True )
def librarian_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...

'''
#@login_required()
#@permission_required('catalog.can_mark_returned', raise_exception=True)
class AllLoandBooksListView(PermissionRequiredMixin, generic.ListView):
#def AllLoandBooksListView(request):
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'
    #permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/all_bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

#from catalog.forms import RenewBookForm
from .forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-loand-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.add_author', )
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    #initial = {'date_of_death': '11/06/2020'}
    initial = {'date_of_birth': datetime.date.today()}



class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_author'
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)



class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_author'
    model = Author
    success_url = reverse_lazy('authors')



class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_book'
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    initial = {'language': 'English'}


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_book'
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_book'
    model = Book
    success_url = reverse_lazy('books')


class BookInstanceDetailView(generic.DetailView):
    model = BookInstance

def bookinstance_detail_view(request, primary_key):
    bookinstance = get_object_or_404(BookInstance, pk=primary_key)
    return render(request, 'catalog/bookinstance_detail.html', context={'bookinstance': bookinstance})


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_bookinstance'
    model = BookInstance
    fields = ['book', 'imprint', 'due_back', 'borrower', 'status']
    initial = {'due_back': datetime.date.today(), 'status': 'm'}


class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_bookinstance'
    model = BookInstance
    fields = '__all__' # Not recommended (potential security issue if more fields added)


class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_bookinstance'
    model = BookInstance
    success_url = reverse_lazy('books')