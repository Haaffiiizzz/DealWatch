# Web Scraping API for Amazon and Best Buy

## Description
This project is a web scraping API designed to scrape product details from Amazon and Best Buy. The API supports scraping individual product pages or Amazon wishlists. Data was initially stored in a PostgreSQL database, with user authentication set up, though the database connection has been temporarily removed.

This standalone project has significantly enhanced my skills in web scraping and API development. In the future, I plan to use this API as a foundation for building a complete shopping site scraper once I gain more experience in web development.

## Skills and Technologies Utilized
- **FastAPI**  
- **Requests**  
- **Selenium**  
- **PostgreSQL**  
- **SQLAlchemy**  
- **RESTful API Development**  
- **Web Scraping**  
- **Postman**

## Features
- Scrapes product details from Amazon and Best Buy given a product link.
- Supports scraping Amazon wishlists.
- User authentication for API endpoints.
- Modular design for future enhancements.

## Future Plans
Once I learn more on web development, I plan to:
- Create a website interface for this API.
- Add more features to build a comprehensive shopping site scraper.

## How to Run
1. Clone this repository:
   ```bash
   git clone <repository-url>
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
3. Install Dependencies:
   ```bash
   uvicorn app.main:app --reload

## Notes
- Database connection has been temporarily removed for simplicity.

Feel free to contribute or provide feedback!


