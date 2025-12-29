🏗️ Architecture
The application follows a standard Client-Server model:

The Tkinter app captures user input and sends JSON payloads.

FastAPI receives the requests and interacts with PostgreSQL using SQLAlchemy.

The database returns the record, and the API sends a structured response back to the GUI