
## Picture Puzzle: BUET CSE FEST 2022  
This repository contains the source code of Picture Puzzle Website for BUET CSE FEST 2022.  
  
## Project Configuration  
Create a `.env`file in the base directory. Add the mentioned variables in the file  

    WEB_CONCURRENCY= <number of web concurrency>
    SERVER = <if the code is in production>
    DEBUG = <set debug to true or false>
    SECRECT_KEY = <secret key for production>
    LEADERBOARD_PAGE = <how many users to load per page in leaderboard page>
    
    CONTEST_STARTED = <set if the contest has started>
    CONTEST_ENDED = <set if the contest has ended>
    SHOMOBAY_SHOMITI = <set Shomobay to true or false>
    
    MEAN = <mean value>
    DEVIATION = <deviation value>
    SPREAD = <spread value>
    SCALE = <scaling value>
    TRANSITION00 = <transition00 value, -cheat(t+1)|-cheat(t)>
    TRANSITION01 = <transition01 value, -cheat(t+1)|+cheat(t)>
    TRANSITION10 = <transition10 value, +cheat(t+1)|-cheat(t)>
    TRANSITION11 = <transition11 value, +cheat(t+1)|+cheat(t)>
    EMISSION00 = <emission00 value, +time(t)|-cheat(t)>
    EMISSION01 = <emission01 value,  -time(t)|-cheat(t)>
    THRESHOLD = <threshold value>
    START_PROB = <strating probability>
    
    DB_HOST = <database host address>
    DB_PORT = <database connection port>
    DB_USER = <database username>
    DB_PASS = <database password>
    DB_NAME = <database name>
    
    MEME_WRONG = <after every MEME_WRONG unsuccessful submissions failure meme is shown>
    SHOW_MEME = <true or false>
    SHOW_HACK = <true or false>
    SHOW_SHOMITI = <true or false>

    
    


  

  
## How To Run  
1. Clone this project  
2. Create a virtual environment in the cloned folder by `python3 -m venv picture_puzzle` in terminal and activate it  
3. Install requirements by `pip install -r requirements.txt`  
4. Make sure you have MySQL installed in your system.
5. To create the database, run `python3 manage.py makemigrations` and `python3 manage.py migrate`  
6. Run the server by `python3 manage.py runserver`