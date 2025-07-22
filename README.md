# TechHive Backend

TechHive is a feature-rich Django REST API for an e-commerce platform, supporting user authentication, product management, categories/subcategories, cart, orders, reviews, and more.

---

## Features

### Authentication & User Management (`userAuth`)
- Custom user model with extended fields.
- JWT authentication (secure, stateless).
- Registration, login, logout, password reset, and email verification (via `django-rest-registration`).
- OTP support for sensitive actions.
- Admin and regular user roles.

### Product & Category Management (`products`)
- Products with name, description, price, stock, image, and rating.
- Categories with parent-child (subcategory) relationships (e.g., Electronics > Watches).
- Nested category serialization for easy API consumption.
- Only admins can add/update/delete products and categories; all users can view.

### Cart (`cart`)
- Add, update, and remove products from the cart.
- Cart is user-specific and persists across sessions.

### Orders (`orders`)
- Place orders from cart contents.
- Order history and status tracking per user.

### Reviews (`reviews`)
- Users can leave reviews and ratings for products.
- Product model tracks average rating, review count, positive/negative review counts.
- Sentiment analysis support (if implemented).

### Core (`core`)
- Placeholder for project-wide signals, utilities, or settings.

### Security
- JWT authentication for all endpoints.
- CSRF protection.
- CORS support for frontend integration.
- Password validation and email verification.
- Environment variables for sensitive settings.

### API Documentation
- **Swagger/OpenAPI** auto-generated docs via `drf_yasg`.
- Visit `/swagger/` or `/redoc/` for interactive API docs.

### Signals
- (If implemented) Signals for updating product ratings, sending notifications, etc.

---

## Tech Stack

- Django & Django REST Framework
- JWT (via `rest_framework_simplejwt`)
- drf-yasg (Swagger docs)
- django-rest-registration (auth flows)
- SQLite (default, easy to switch to PostgreSQL/MySQL)
- CORS, dotenv, Django Filters

---

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/httpsMansoor/Tech-Hives-Backend.git
   cd Tech-Hives-Backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env` and set your secrets (email, DB, etc).

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Usage

- Access the API at `http://localhost:8000/`
- Swagger docs at `http://localhost:8000/swagger/`
- Media files served from `/media/`
- Admin panel at `/admin/`

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](LICENSE) 