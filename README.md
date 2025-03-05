# Classroom Booking System

## Greeting Words

Welcome to Classroom Booking System project using Flask, Pydantic and MongoDB.

### The system is rich with:

- **Comformatble classroom booking process**
- **Access control with Admin**
- **WebSocket handshake mechanism**
- **MongoDB integration with AsyncIOMotorClient and mongoengine**

---

## Folder Structure

### Root-Level Files:
- **`.env`**: Environment for storing secret variable (e. g. Database URL).
- **`README.md`**: Information about project and guide to it.
- **`requirements.txt`**: To have installed all modules and packages for this project.

### Application directory (`app/`):

- **`main.py`**: Main part of the the.
- **`__init__.py`**: For making directory, the package.
- **`config`**: App configuration files.
  - **`settings.py`**: Configuration settings, e.g. database connection URL.
- **`database`**: Manages database connection.
  - **`session.py`**: MongoDB set up.
- **`models`**: Contains MongoDB Document type models.
  - Examples: `schedule.py`, `student.py`.
- **`routers`**: Contains API endpoint routers.
  - Examples: `admin.py`, `guest.py`, `student.py`.
- **`schemes`**: Includes pydantic schemes for request / response validation and setialization.
  - Examples: `schedule.py`, `student.py`.
- **`servies`**: Business logic functions for reusability.
  - Examples: `active_conn.py`, `admin.py`, `guest.py`, `notifications.py`, `student.py`
- **`utils`**: Utility functions like api key and secret_code generation, authentication.
  - Examples: `api_and_secret.py`, `auth.py`, `broadcast.py`.

---

### Setup instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/ArthurJraghatspanyan/classrooms_booking
    cd classrooms_booking
    ```
2. Create and configure the `.env` file with necessary variables:
    ```
    MONGO_URI=<your_database-uri>
    SECRET_KEY=<your_secrey_key>
    ADMIN_PASSWORD=<your_admin_password>
    SLACK_TOKEN=<slack_bot_token_for_notifications>
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Start Flask server in couple of ways:
    ```
    uvicorn app.main:app  --reload
    ```

    or

    ```
    hypercorn app.main:app --reload
    ```

    or

    ```
    pip install watchdog
    watchmedo auto-restart --pattern="*.py" --recursive -- hypercorn app.main:app --reload
    ```

    With the last and first ones, server starts automatically, even with syntax errors in the code.