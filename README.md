# cs425-final-project-application

The final project for our CS425 class at IIT (see [Associated GitHub Repo](https://github.com/xenten9/cs425-final-project-application)).  

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

