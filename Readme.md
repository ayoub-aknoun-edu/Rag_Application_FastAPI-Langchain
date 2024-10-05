# Rag Application Langchain/FastAPI

## Description

Rag Application is a web application built using FastAPI and Langchain. It provides various functionalities related to data processing, NLP, and project management.

## Features

- **Data Upload and Processing**: Upload and process data files.
- **NLP Operations**: Perform NLP operations such as indexing and searching.
- **Project Management**: Manage projects and their associated data.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/rag-application.git
    cd rag-application
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Copy the `.env.example` file to `.env` and fill in the necessary values.
    ```sh
    cp src/.env.example src/.env
    ```

## Usage

1. Start the FastAPI server:
    ```sh
    uvicorn src.main:app --reload
    ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Docker

1. Build the Docker image:
    ```sh
    docker-compose build
    ```

2. Run the Docker container:
    ```sh
    docker-compose up
    ```

3. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Project Structure
    
```text
├── .gitignore 
├── docker/ 
│ ├── .env 
│ ├── .env.example 
│ ├── .gitignore 
│ └── docker-compose.yml 
├── Readme.md 
├── requirements.txt 
├── src/ 
  ├── .env 
  ├── .env.example 
  ├── .gitignore 
  ├── assets/ 
  │ ├── .gitignore 
  │ ├── database/ 
  │ └── files/ 
  ├── controllers/ 
  │ ├── init.py 
  │ ├── BaseController.py 
  │ ├── DataController.py 
  │ ├── NLPController.py 
  │ └── ProcessController.py 
  ├── helpers/ 
  │ ├── init.py 
  │ └── config.py 
  ├── main.py 
  ├── models/ 
  │ ├── init.py 
  │ └── ... 
  ├── routes/ 
  │ ├── base.py 
  │ ├── data.py 
  │ └── nlp.py 
  └── stores/ 
```

## API Endpoints

### Data Routes

- **Upload Data**: `POST /api/v1/data/upload/{project_id}`
- **Process Data**: `POST /api/v1/data/process/{project_id}`

### NLP Routes

- **Index Project**: `POST /api/v1/nlp/index/push/{project_id}`
- **Get Project Index Info**: `GET /api/v1/nlp/index/info/{project_id}`
- **Search Index**: `POST /api/v1/nlp/index/search/{project_id}`

### Base Routes

- **Welcome**: `GET /api/v1/`

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License.