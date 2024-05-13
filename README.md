# CourseMe API

## Overview

CourseMe API is a RESTful web service developed as part of laboratory work nr.7 for the Web Programming course. It provides a set of endpoints for CRUD operations used in managing and retrieving course information. The API is documented with Swagger to facilitate easy integration and testing.

## Prerequisites

- Python 3.8 or higher
- pip3 for package installation

## Installation

Follow these steps to get your development environment set up:

1. Clone the repository:
   ```bash
   git clone git@github.com:MaxCojocari/tum-web-lab7.git
   cd tum-web-lab7
   ```
2. Set up a Python virtual environment:
   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Initialize DB with mock data:
   ```bash
   python3 init_db.py
   ```  

## Running API

```bash
python3 app.py
```

This will start the API server on http://localhost:5000/.

## Swagger

Access the Swagger UI to interact with the API at http://localhost:5000/apidocs/.
