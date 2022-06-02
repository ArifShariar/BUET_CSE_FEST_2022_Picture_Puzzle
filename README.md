## Picture Puzzle: BUET CSE FEST 2022
This repository contains the source code of Picture Puzzle Website for BUET CSE FEST 2022.

## Project Configuration
Create a `.env`file in the base directory. Add the mentioned variables in the file
 - SECRET_KEY=<your_secret_key>

## How To Run
1. Clone this project
2. Create a virtual environment in the cloned folder by `python3 -m venv picture_puzzle` in terminal and activate it
3. Install requirements by `pip install -r requirements.txt`
4. To create the database, run `python3 manage.py makemigrations` and `python3 manage.py migrate`
5. Run the server by `python3 manage.py runserver`