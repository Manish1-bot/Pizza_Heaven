# Online Pizza Shopping Portal

A fully functional, production-ready online pizza ordering web application built using Python (Flask), SQLAlchemy, and Bootstrap 5.

## Features Let's Create
### Customer Interface
- User Registration & Authentication
- Graphical Menu Display with categories (Veg/Non-Veg)
- Dynamic Cart Management (add, update quantities, remove)
- Checkout Flow with Delivery details
- Online Payment Sandbox Integration (Razorpay)
- Auto-generated receipt and order history
- Responsive UI (Mobile friendly)

### Admin Interface
- Admin Dashboard with metrics and dynamic statistics
- Complete Pizza Management (Add, Edit, Delete, Stock status)
- Order Management and Status updating
- Modern Admin UI design

## Requirements
- Python 3.8+
- Requirements listed in `requirements.txt`

## Installation & Setup

1. **Clone or navigate to the project repository.**
2. **Set up a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**
   The project contains a `.env` file where environment variables are stored, including `SECRET_KEY`, Database URI, and Razorpay API Keys. Make sure they are correctly loaded.

5. **Run the Application**
   ```bash
   python run.py
   ```
   *Note: Upon running for the first time, it will automatically setup the SQLite database, populate it with 10 sample pizzas, and create an Admin user.*

## Default Test Credentials
- Admin Email: `admin@pizza.com`
- Password: `admin123`

## Payment Testing (Razorpay)
Use the Razorpay Test Card Details for checkout:
- Card Number: `4111 1111 1111 1111`
- Expiry Date: Any future date (e.g. `12/25`)
- CVV: Any 3 digit number (e.g. `123`)

## Authors
Created by Antigravity (Google Advanced Agentic Coding Team).
