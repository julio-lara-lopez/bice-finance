# Expense Management App

This application helps you track and categorize your expenses by uploading Excel files from your credit card and checking account.

## How to Run the Application

### 1. Start the Backend

First, you'll need to install `uv`. You can find instructions for your OS in the [official documentation](https://github.com/astral-sh/uv).

Once `uv` is installed, navigate to the `backend` directory in your terminal:

```bash
cd backend
```

Then, create a virtual environment and install the necessary Python packages:

```bash
uv venv
uv pip sync pyproject.toml
```

Finally, run the FastAPI application:

```bash
uv run uvicorn main:app --reload
```

The backend will be running at `http://localhost:8000`.

### 2. Start the Frontend

Open a new terminal and navigate to the `frontend` directory:

```bash
cd frontend
```

Install the required npm packages:

```bash
npm install
```

Now, start the React application:

```bash
npm start
```

The frontend will open automatically in your browser at `http://localhost:3000`.

## How to Use

1.  Open the application in your browser.
2.  Click the "Choose File" button to select an Excel file with your expenses.
3.  Click the "Upload" button to upload and process the file.
4.  The categorized expenses will be displayed in the table below.
5.  Click the "Refresh Expenses" button to update the table with the latest data.

## Next Steps

To make this application more robust, the following features could be added:

*   **Database Integration:** Store the expenses in a database (like PostgreSQL or SQLite) to persist the data.
*   **User Authentication:** Add user accounts to allow multiple users to track their expenses.
*   **Data Visualization:** Create charts and graphs to visualize the expenses by category, date, etc.
*   **Deployment:** Deploy the application to a cloud service (like Heroku or AWS) to make it accessible from anywhere.
