# TechHive Backend

This is the backend for the TechHive project, built with Django.

## Project Structure
- `manage.py`: Django project management script
- `products/`, `cart/`, `orders/`, `reviews/`, `userAuth/`, `core/`: Django apps
- `TechHive/`: Project settings and configuration
- `db.sqlite3`: SQLite database (for development)

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/httpsMansoor/Tech-Hives-Backend.git
   cd Tech-Hives-Backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the API at `http://localhost:8000/`
- Media files are served from `/media/`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE) 