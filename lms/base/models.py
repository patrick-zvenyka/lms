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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

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
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_fine(self, fine_per_day=0.50):
        """
        Calculate overdue fine if the book is not returned by the due date.
        """
        if self.status == 'borrowed' and date.today() > self.due_date:
            overdue_days = (date.today() - self.due_date).days
            return round(overdue_days * fine_per_day, 2)
        return self.fine

    def save(self, *args, **kwargs):
        """
        Update fine and ensure return_date is set when the book is returned.
        """
        if self.status == 'borrowed' and date.today() > self.due_date:
            self.fine = self.calculate_fine()
        if self.status == 'returned' and not self.return_date:
            self.return_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} borrowed {self.book}"
