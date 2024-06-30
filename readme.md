# Define the content for the README.md file
readme_content = """
# PrimeSubscape

PrimeSubscape is a web application designed to manage Amazon Prime subscription data. The application allows users to view, query, and manage user data effectively.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/PrimeSubscape.git
    cd PrimeSubscape
    ```

2. **Set up a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database:**

    ```bash
    python app/database_init.py
    ```

## Usage

1. **Run the application:**

    ```bash
    flask run
    ```

2. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000`.

## Project Structure

PrimeSubscape/
│
├── app/
│   ├── __init__.py          # Initializes the Flask application
│   ├── database_init.py     # Script to initialize the database
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes
│   ├── static/
│   │   ├── background1.jpg  # Static images
│   │   ├── script.js        # JavaScript files
│   │   └── style.css        # CSS files
│   └── templates/
│       ├── edit_user.html   # Template for editing user details
│       ├── index.html       # Main page template
│       └── querytemplate.html # Template for querying data
│
├── csv_prime_user/
│   └── amazon_prime_users.csv # Sample user data in CSV format
│
├── .gitignore               # Git ignore file
├── requirements.txt         # Python dependencies
└── README.md                # Project README file
