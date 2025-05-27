# Agro Chatbot

This project is a chatbot designed to discuss agro-related topics. It leverages the Gemini 2.0 Flash model from Google to provide informative and engaging conversations.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+:**  Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **pip:** Python's package installer (usually included with Python).

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <todo>
    cd <todo>
    ```

2.  **Create a conda environment (recommended):**

    ```bash
    conda create --name langchain python=3.9 # or your desired Python version
    conda activate langchain
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**

    *   Create a `.env` file in the root directory of the project.
    *   Add the following variables to the `.env` file:

        ```
        GOOGLE_API_KEY=<Your_Google_API_Key>
        GOOGLE_MODEL=gemini-2.0-flash
        TEMPERATURE=0.5
        STREAMING=True
        ```

        *   Replace `<Your_Google_API_Key>` with your actual Google API key.  You'll need to obtain this from the Google Cloud Console.
        *   `GOOGLE_MODEL`: Specifies the Gemini model to use (default: `gemini-2.0-flash`).
        *   `TEMPERATURE`: Controls the randomness of the model's output (default: `0.5`).  Lower values make the output more predictable, higher values make it more creative.
        *   `STREAMING`: Enables or disables streaming responses from the model (default: `True`).

    **Important:**  Never commit your `.env` file to version control.  Add it to your `.gitignore` file.

## Project Structure

agro-chatbot/
├── app/                # Main application directory
│   ├── pycache/    # Python cache files (ignore)
│   ├── models/         # Data models (e.g., for chat messages)
│   │   └── chat_models.py
│   ├── public/         # Static files (e.g., HTML, CSS, JavaScript)
│   │   └── index.html
│   ├── routes/         # API route definitions
│   │   ├── pycache/
│   │   ├── chat.py     # Chat-related API endpoints
│   │   └── home.py     # Home/index route
│   ├── services/       # Business logic and external service integrations
│   │   ├── pycache/
│   │   └── chat_service.py # Logic for interacting with the Gemini model
│   ├── utils/          # Utility functions and helpers
│   ├── config.py       # Configuration settings
│   ├── dependencies.py # Dependency injection setup
│   └── main.py         # FastAPI application entry point
├── .env                # Environment variables (API keys, settings)
├── README.md           # This file
└── requirements.txt    # Python dependencies

## Running the Application

1.  **Navigate to the project root directory in your terminal.**

2.  **Run the application using Uvicorn:**

    ```bash
    uvicorn app.main:app --reload
    ```

    *   `app.main`: Specifies the module containing the FastAPI application.
    *   `app`:  Specifies the variable name of the FastAPI instance within `main.py`.  If your app instance has a different name, adjust accordingly.
    *   `--reload`: Enables automatic reloading on code changes (for development).

3.  **Access the application in your browser:**

    *   Open your web browser and go to `http://127.0.0.1:8000` (or the address shown in the Uvicorn output).

## API Endpoints TODO: MORE DETAIL

*   **`/` (GET):**  Serves the `index.html` file (likely the chatbot interface). Defined in `routes/home.py`.
*   **`/chat` (POST):**  Handles chat requests.  Takes user input and sends it to the Gemini model via the `chat_service`. Defined in `routes/chat.py`.

## Key Components

*   **`app/main.py`:**  The main entry point for the FastAPI application.  It initializes the FastAPI app, sets up middleware, and includes the API routers.
*   **`app/routes/chat.py`:** Defines the `/chat` API endpoint.  It receives user messages, passes them to the `chat_service`, and returns the model's response.
*   **`app/services/chat_service.py`:** Contains the logic for interacting with the Gemini model.  It handles authentication, sends requests to the model, and processes the responses.
*   **`app/config.py`:**  Loads configuration settings from environment variables using the `Settings` class.
*   **`.env`:** Stores sensitive information like API keys and configuration settings.

## Configuration

The application is configured using environment variables.  The following variables are used:

*   `GOOGLE_API_KEY`:  **Required.**  Your Google API key.
*   `GOOGLE_MODEL`:  The Gemini model to use (default: `gemini-2.0-flash`).
*   `TEMPERATURE`: The temperature setting for the model (default: `0.5`).
*   `STREAMING`:  Whether to enable streaming responses (default: `True`).

## Deployment

The application can be deployed to various platforms, including:

*   **Google Cloud Platform (GCP):**  Use Cloud Run or App Engine.
*   **Heroku:**  A popular platform-as-a-service.
*   **AWS:**  Use Elastic Beanstalk or ECS.
*   **Docker:**  Containerize the application for easy deployment.

**Example Deployment to Google Cloud Run:**

1.  **Create a Dockerfile:**

    ```dockerfile
    FROM python:3.9-slim-buster

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
    ```

2.  **Build the Docker image:**

    ```bash
    docker build -t agro-chatbot .
    ```

3.  **Push the image to Google Container Registry (GCR):**

    ```bash
    docker tag agro-chatbot gcr.io/<your_gcp_project_id>/agro-chatbot
    docker push gcr.io/<your_gcp_project_id>/agro-chatbot
    ```

4.  **Deploy to Cloud Run:**

    ```bash
    gcloud run deploy --image gcr.io/<your_gcp_project_id>/agro-chatbot --platform managed --region <your_gcp_region>
    ```

    *   Replace `<your_gcp_project_id>` with your Google Cloud project ID.
    *   Replace `<your_gcp_region>` with your desired Google Cloud region.

5.  **Set the `GOOGLE_API_KEY` environment variable in Cloud Run.**  You can do this through the Cloud Console or using the `gcloud` command-line tool.

## Contributing

Contributions are welcome!  Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Write tests for your changes.
5.  Submit a pull request.
