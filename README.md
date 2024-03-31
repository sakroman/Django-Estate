# Django Estate Website
## Description

The Estate Website is a web application developed using Python Django framework. It serves as a platform for listing and browsing real estate properties. The website provides users with features such as property search, detailed property listings, and contact forms for inquiries.

## Features

1. User-friendly interface for browsing and searching properties.
2. Detailed property listings with descriptions, images, and specifications.
3. Property search functionality with filters for location, price, property type, etc.
4. Contact forms for users to inquire about properties or schedule viewings.

## Technologies Used

1. Python Django: Backend framework for building the web application.
2. Bootstrap: Frontend framework for responsive and mobile-first design.
3. Font Awesome: Icon toolkit for adding scalable vector icons to the website.
4. JavaScript: Programming language for enhancing frontend interactivity and functionality.

## Installation

1. Clone the repository:

    
```bash
git clone https://github.com/your-username/estate-website.git
```
2. Install Python dependencies:

```
pip install -r requirements.txt
```

3. Import the SQL Dump File:
    Run the following command to import the SQL dumpfile into your PostgreSQL database:

```php
psql -U <username> -d <database_name> -f estate_dump.sql
```

**Replace <username> with your PostgreSQL username and <database_name> with the name of the database where you want to import the data. The process is similar with different database management systems.**

**Verify Data: Once the import process is complete, verify that the data has been successfully imported into your database by querying the tables.** <br />

5. Apply database migrations:

```
python manage.py migrate
```

6. Create a superuser (admin) account:

```
python manage.py createsuperuser
```

7. Start the development server:

```
python manage.py runserver
```

Access the website at http://localhost:8000 in your web browser.

# Warning! For the contact form to work you have to enter your email and password in settings.py
