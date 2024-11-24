# Django Anime Project with MongoDB
## Setup
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv env
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver
## Update the database
1. Open the Django shell:
python manage.py shell
2. Execute commands below:
``` bash
from anime.utils import fetch
from time import sleep

for id in range(1,1000):
    fetch(id)
    sleep(0.5)
