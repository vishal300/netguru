# netguru
basic car makes and models database interacting with an external API.

Open Terminal (Applications > Utilities > Terminal)

Enter the following commands: NOTE: The command sudo will require an admin password. The same password you use to install other programs. Typing will be hidden

 1. Install Pip. (Python Package Installer):
          sudo easy_install pip
          ```
  2. Install virtualenv:

          ```
          sudo pip install virtualenv
          ```                   
Create a new virtualenv:

         ```
         virtualenv lish -p python3
         ```
Activate virtualenv:

         ```
         source bin/activate
         ```
         The result in Terminal should be something like:
Install Django: pip install django

Install requirements: pip install -r requirements.txt python manage.py makemigrations python manage.py migrate
Run Command:
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
