# LITReview

> ### ***Disclaimer :***
> *This project, including what is included in this README, is a school project responding to a 
> fictional scenario and has no other purpose.  
> In light of this, the database and medias have been included in the project.*

Minimum Viable Product version of a web app whose purpose is to allow users to ask for or make reviews of books or articles.

## Installation

1. Clone this repository to your local machine
2. I strongly recommend you to set up your virtual environment (using for example *venv* or *pipenv*)  
If you need a reminder on how to set up a virtual environment using venv, you can find the documentation [here](https://docs.python.org/3/library/venv.html).
3. Activate your virtual environment and install the requirements.  
You can run `pip install -r requirements.txt` or install the following prerequisites one by one:
    - django
    - django-bootstrap5
    - django-bootstrap-icons
    - pillow
4. From the root of the repo, go to litrevu and run `python manage.py runserver`.  
The terminal give you the address of the local server you just started in a line like:
    > Starting development server at http://127.0.0.1:8000/
5. In a web browser, add `login/` to the given address to access the login page:
    > http://127.0.0.1:8000/login/
6. Use one of the credentials available in the next part of this README to login.

(*Developed and tested under Python 3.11.2*)

## Credentials

To log in this school project you can chose from the following users (case sensitive):
- **_dayrise_**
- **_mercedes_**
- **_toto_**
- **_test_user_1_**
- **_test_user_2_**
- **_test_user_3_**

`dayrise` is the admin user and his password is `P@ssw0rd`. All the others users have `Azerty123` as password.  
I recommend to use **_mercedes_** credentials for a first overview of this MVP.