# Flask Project

A web application built with Python and Flask.

## Prerequisites

Before running this project, ensure you have the following installed:
* Python 3.8 or higher
* Git

## Getting Started

Follow these steps to set up and run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone -b "impl-ui/visa" <repository-url>
cd <project-folder-name>
```

### 2. Set Up the Virtual Environment
Create a fresh virtual environment to manage dependencies locally.

  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 3. Install Dependencies
Ensure your virtual environment is active, then install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Since configuration files are ignored by Git, you must create a local environment file.

1. Create a file named `.env` in the root directory.

### 5. Run the Application
Start the Flask development server:
```bash
flask run
```
The application will be available at `http://127.0.0`.