# cs425-final-project-application

The final project for our CS425 class at IIT (see [Associated GitHub Repo](https://github.com/xenten9/cs425-final-project-application)).  

## How to load database

In order to load the database simply run the below command:

```cmd
mysql -u root -p matthew_family_realty < ./datafiles/database/dump.sql
```

and then enter the password to your local database when prompted.
Furthermore your password must be stored in the ```./password``` file at the root of this project directory. Alternatively you can enter your pass word in the command prompy when asked; However, this can be finnicky.

## How to run main.py

First in the main director which this md file is located create a file  ```./password``` with no file extension.
This file should contain the plain text password for ease of use; However, if not provided a prompt can instead be filled in within the program; However, the program will not remember the password between launches.

In order to run the program one should first create a new virtual environment for python and then run

```cmd
pip install -r requirements.txt
```

in order to donload all required packages for the program to run. Furethermore there needs to be a local database containing all of the csv files stored inside of ```./datafiles/```. Inside the folder is a ```./datafiles/load_data.sql``` file which when run succesfully will search for the csv files inside of ```C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/```. If they are all found it will fully form the database neccesary for the project to run. If not then the tables should still form, but will not contain any data.

In order to run the project simply execute the command below from the project root(ensures proper working directory).

```cmd
py main.py
```

## How to run sql_test.py

Running ```./sql_test.py``` is straight forward and if you have questions for options run the file with the ```-h``` flag for help.

## If you run into issues...

1. Make sure all commands are being run in the windows command prompt and not the powershell
2. Double check the commands are typed properly.
3. If the gui section freezes on loading, it is probably waiting for you to enter the password in the terminal.
4. Make sure that all programs neccesary such as python and mysql database are installed, functioning, and have the neccesary windows system paths configured.
5. Try a solution based on what you are used to keeping in mind what the commands provided do, for example entering the mysql command prompt for database import could work better if you are more familiar.
6. If all else fails, email me at ```jraynor@hawk.iit.edu```, I am open to arranging a meeting if that works best.

