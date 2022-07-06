

## Picture Puzzle: BUET CSE FEST 2022  
This repository contains the source code of Picture Puzzle Website for BUET CSE FEST 2022.  
  
## Project Configuration  
Create a `.env`file in the base directory. Add the mentioned variables in the file  


    
    DB_HOST = <database host address>
    DB_PORT = <database connection port>
    DB_USER = <database username>
    DB_PASS = <database password>
    DB_NAME = <database name>

    
    
## Database Stuff
```sql
CREATE DATABASE db_name
CHARACTER SET charset_name
COLLATE collation_name

ALTER DATABASE db_name
CHARACTER SET charset_name
COLLATE collation_name
```


  

  
## How To Run  
1. Clone this project  
2. Create a virtual environment in the cloned folder by `python3 -m venv picture_puzzle` in terminal and activate it  
3. Install requirements by `pip install -r requirements.txt`  
4. Make sure you have MySQL installed in your system.
5. To create the database, run `python3 manage.py makemigrations` and `python3 manage.py migrate`  
6. Run the server by `python3 manage.py runserver`
