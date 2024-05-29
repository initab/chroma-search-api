# Chroma Search API

A HTTP frontend to query a Chroma Vector Database

## Overview

The Chroma Search API provides a simple way to query a Chroma Vector Database using HTTP requests. It takes
two inputs in the body of the POST request: "prompt" and "num_results". The API uses the "prompt" input to
query the database and returns as many results as specified by the "num_results" input.

## Get Started

To start using the Chroma Search API, you will need:

1. **Python 3.11 or greater**: Make sure your Python version meets this requirement.
2. **A Python virtual environment setup**: Install a virtual environment tool like `virtualenv` or `conda`,
   and set up a new environment.
3. **Activated virtual environment**: Activate the virtual environment using the command provided by the tool
   you chose.

Once your virtual environment is active, you can install the requirements for the project by running:

```
pip install -r requirements.txt
```

This will install all the necessary dependencies listed in the `requirements.txt` file.

## Usage

To use the Chroma Search API, send a POST request to the API endpoint with the following format:

```json
{
  "prompt": "<your prompt here>",
  "num_results": "<number of results you want, (number type)>"
}
```

Replace `<your prompt here>` with the text you want to query the database for. Replace `<number of results
you want>` with the number of results you want returned.

## API Endpoints

The Chroma Search API has a single endpoint: `/search`. This is where you should send your POST request with
the prompt and number of results as described above.

### Example Request

Here is an example of what a valid request might look like:

```shell
curl -X POST \
  http://localhost:8000/search \
  -H 'Content-Type: application/json' \
  -d '{
        "prompt": "What is the meaning of life?",
        "num_results": 5
      }'
```

### Example Response

The response to this request might look like:

```json
{
  "ids": [
    "12345",
    "67890"
  ],
  "distances": [
    0.8,
    0.6
  ],
  "documents": [
    "Meaning of Life is 42 - Brian",
    "Life has no meaning - Nietzsche"
  ],
  "metadata": [
    {
      "author": "John Doe",
      "date_published": "2022-01-01"
    },
    {
      "author": "Jane Doe",
      "date_published": "2021-01-01"
    }
  ]
}
```

In this example, the response is a JSON object that contains four keys: `ids`, `distances`, `documents`, and
`metadata`. The value of each key is an array or object as described above.