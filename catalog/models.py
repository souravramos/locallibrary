from django.db import models
from django.urls import reverse # used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from PIL import Image
# Create your models here.

class Genre(models.Model):
    """ Model representing a book genre. """
    name = models.CharField(max_length=200, unique=True, help_text= 'Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """ String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """ Returns the url to access a particular genre instance """
        return reverse('genre-detail', args=[str(self.id)])

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """  Returns the ulr to access a particular genre instance """
        return reverse('language-detail', args=[str(self.id)])

class Book(models.Model):
    """ Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    image = models.ImageField(upload_to='media/book_covers', default='default.jpg')

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as as string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, help_text='Select a language for this book')

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number<a/>', null=True, blank=True)

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already bee defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    edition = models.CharField('Edition', max_length=20, null=True, blank=True)

    price = models.IntegerField('Price(INR)', null=True, blank=True)

    buy_online = models.CharField('Buy Online', max_length=200, null=True, blank=True, help_text='Enter a link to buy this book online')

    def __str__(self):
        """ String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """ Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """ Create a string for the Genre. This is required to display genre in Admin. """
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """ Model representing a specific copy of a book (i.e. that can be borrowed from the library )."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length=1, 
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """ String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """ Model representing an author. """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    details = models.TextField(null=True, blank=True, max_length=2000)
    image = models.ImageField(upload_to='media/author_photos', default='default.jpg')

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        """ Returns the url to access a particular author instance """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """ String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

    def save(self, *args, **kwargs):
        super(Author, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)