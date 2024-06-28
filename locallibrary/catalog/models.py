from django.db import models

from django.urls import reverse

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

import uuid #required for unique book instances

class Genre(models.Model):
    #Model representing a book genre

    name = models.CharField(
        max_length = 100,
        unique = True,
        help_text = "Enter a book genre"
    )

    def __str__(self):
        """String for representing model object"""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular genre instance"""
        return reverse('genre-detail', args = [str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists"
            ),
        ]

class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length = 100)
    author = models.ForeignKey('Author', on_delete = models.RESTRICT, null = True)
    
    #Foreign key used because book can only have one author but an author
    #can have multiple books.

    summary = models.TextField(
        max_length = 1000,
        help_text = "Give a short description of the book"
    )

    isbn = models.CharField(
        'ISBN',
        max_length = 15,
        unique = True,
        help_text = '13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    #ManytoManyField used because genre can contain many books.
    #Books can cover many genres

    genre = models.ManyToManyField(
        Genre,
        help_text = "Select a genre for the book"
    )

    def __str__(self):
        """String for representing model object"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book"""
        return reverse('book-detail', args = [str(self.id)])
    
class BookInstance(models.Model):
    """Model representing a specific copy of book (i.e. that can be borrowed from library)"""
    
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        help_text = "Unique ID for the book"
    )
    book = models.ForeignKey(
        'Book',
        on_delete = models.RESTRICT,
        null = True
    )
    imprint = models.CharField(max_length = 100)
    due_back = models.DateField(null = True, blank = True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    
class Language(models.Model):
    """Model representing language"""

    lang = models.CharField(
        max_length = 100,
        unique = True,
        help_text = "Enter the language of the book"
    )
    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.lang
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                lang = 'language_name_case_insensitive_unique',
                violation_error_message = "Language already exists"
            ),
        ]