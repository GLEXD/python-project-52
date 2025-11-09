### Hexlet tests and linter status:
[![Actions Status](https://github.com/GLEXD/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/GLEXD/python-project-52/actions)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=GLEXD_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=GLEXD_python-project-52)
[![Python CI](https://github.com/GLEXD/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/GLEXD/python-project-52/actions/workflows/ci.yml)

# Project was made for Hexlet by Gleb Burimov
Task Manager is a task management system. It allows you to set tasks, assign performers, and change their statuses.

### You can view application on the website: [Task Manager](https://task-manager-5psv.onrender.com)

## Features
* User registration and authentication  
* CRUD operations for:
  * Tasks (creation, editing, deletion, assignment of performers)  
  * Statuses (task statuses: new, in progress, done, etc.)
  * Labels (tags for tasks)  
* Restrictions on deleting entities if they are used  
* Authorization:
* Tasks can only be deleted by their author  
  * Unauthorized actions are blocked  
* Interface based on Django templates  
* Multilingual support (i18n) 

## Libraries:
* dj-database-url
* django
* django-bootstrap5
* django-filter
* dotenv
* gunicorn
* playwright
* psycopg2-binary
* pytest
* pytest-playwright
* python-dotenv
* rollbar
* whitenoise

## Installation and Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/GLEXD/python-project-52.git
    cd python-project-83
    ```

2. Create `.env` file:
    ```bash
    DATABASE_URL=postgresql://username:password@localhost:5432/dbname
    SECRET_KEY=your_secret_key_here
    ```

3. Install dependencies:
   ```bash
   make install
   ```
   
4. Start application:
   ```bash
   docker-compose up
   ```