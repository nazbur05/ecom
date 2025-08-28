# TechStore E-commerce

A Django-based e-commerce platform for tech products.

## Features
- User registration and authentication
- Customer profile management
- Product catalogue with categories and subcategories
- Add/remove products to favourites and cart
- Place orders with checkout validation
- Responsive UI with category navigation

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## Seeding Sample Data

To add sample categories, subcategories, and products, run:

```
python manage.py shell
```
Then in the shell:

```python
from shop.seed import run
run()
```

This will create example categories, subcategories, and products.