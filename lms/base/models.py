from django.db import models
from datetime import timedelta, date

class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Shelf(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    BOOK_FORM_CHOICES = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
    ]
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    form = models.CharField(max_length=1, choices=BOOK_FORM_CHOICES)  # Corrected this line
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    STUDENT_FORM_CHOICES = [
        ('1E','1E'),
        ('1W','1W'),
        ('1N','1N'),
        ('1S','1S'),
        ('2E','2E'),
        ('2W','2W'),
        ('2N','2N'),
        ('2S','2S'),
        ('3E','3E'),
        ('3W','3W'),
        ('3N','3N'),
        ('3S','3S'),
        ('4E','4E'),
        ('4W','4W'),
        ('4N','4N'),
        ('4S','4S'),
        ('5S','5S'),
        ('5C','5C'),
        ('5A','5A'),
        ('6S','6S'),
        ('6C','6C'),
        ('6A','6A'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    form = models.CharField(max_length=2, choices=STUDENT_FORM_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)  # Due date should be a DateField
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    delayed_days = models.IntegerField(default=0, null=True, blank=True)  # New field for delayed days
    updated_at = models.DateField(auto_now_add=True)

    def calculate_fine(self, fine_per_day=0.50):
        """
        Calculate overdue fine if the book is not returned by the due date.
        """
        if self.status == 'borrowed' and date.today() > self.due_date:
            overdue_days = (date.today() - self.due_date).days
            return round(overdue_days * fine_per_day, 2)
        return self.fine

    def calculate_due_date(self):
        """
        Calculate the due date based on the borrow date.
        This function is called in the save method.
        """
        # Assume the book is due 14 days after borrowing
        return self.borrow_date + timedelta(days=14)

    def calculate_delayed_days(self):
        """
        Calculate days overdue if the book has been returned.
        """
        if self.status == 'returned' and self.return_date:
            delay = (self.return_date - self.due_date).days
            return delay if delay > 0 else 0  # Return 0 if not overdue
        return self.delayed_days

    def save(self, *args, **kwargs):
        """
        Update fine, due_date, delayed_days, and ensure return_date is set when the book is returned.
        """
        # Set due_date if it's not already set
        if not self.due_date:
            self.due_date = self.calculate_due_date()

        # Calculate delayed days if book is returned
        if self.status == 'returned' and self.return_date:
            self.delayed_days = self.calculate_delayed_days()
            if self.delayed_days > 0:
                self.fine = round(self.delayed_days * 0.50, 2)  # Fine for late return

        # If book is still borrowed, calculate fine based on the current date
        if self.status == 'borrowed' and date.today() > self.due_date:
            self.fine = self.calculate_fine()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} borrowed {self.book}"