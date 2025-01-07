from django.db import models
from datetime import timedelta, date

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField()

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
        if self.status == 'borrowed' and date.today() > self.due_date:
            overdue_days = (date.today() - self.due_date).days
            return round(overdue_days * fine_per_day, 2)
        return self.fine

    def save(self, *args, **kwargs):
        # Automatically calculate fine for late returns
        if self.status == 'borrowed' and date.today() > self.due_date:
            self.fine = self.calculate_fine()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} borrowed {self.book}"
