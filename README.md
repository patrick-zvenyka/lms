# Library Management System (LMS)

A simple Library Management System (LMS) built using Django to manage books, borrowing, and returning operations in a library. This project includes features such as adding new books, viewing book history, managing borrowing status, and more.

## Features

- **Book Management**: Add new books with information such as ISBN, title, subject, shelf, and form.
- **Borrowing System**: Students can borrow books, with automatic tracking of due dates, fines, and status.
- **Borrow History**: Keep track of the borrow history of each book, showing all past borrowing transactions.
- **Pagination**: Book history and borrow records are paginated for easier browsing.
- **Admin Panel**: Admin users can manage books, borrow records, and more.
- **Fine Calculation**: Late return of books triggers a fine, which is calculated based on the number of overdue days.

## Technologies Used

- **Django**: Python web framework for building the backend of the system.
- **SQLite**: Database used for storing records of books, students, and borrowing transactions.
- **HTML/CSS**: For frontend rendering and styling of pages.
- **Bootstrap**: For responsive and modern design components.
- **Messages Framework**: To provide feedback to users about errors, success, and notifications.
- **Django ORM**: For managing and querying the database using Django's Object-Relational Mapping (ORM) system.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lms.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and visit `http://127.0.0.1:8000` to view the application.

## Usage

- **Admin Panel**: Access the admin panel by navigating to `http://127.0.0.1:8000/admin/` and log in using the superuser credentials you created.
- **Library Operations**: Use the system to manage books, track borrowing transactions, and calculate fines based on overdue days.

## Screenshots

_(Add some screenshots or GIFs here to showcase the app in action)_

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to your fork (`git push origin feature/your-feature-name`).
6. Create a pull request.


Feel free to replace or modify any sections with additional details specific to your project!
