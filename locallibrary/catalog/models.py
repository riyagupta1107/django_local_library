from django.db import models

from django.urls import reverse

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

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