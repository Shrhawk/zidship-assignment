# ZidShip Assignment
The purpose of this assignment is to make unified interface for a courier system to 
communicate through different courier services and integrate more couriers 
without making interface decisions all over again.
## Database configuration
Edit the [config.py](config.py) file to connect with your database.
### Virtual Environment
Now, create a virtual environment and activate it.
```shell
python -m venv env
source env/bin/activate
```
## Install Dependencies
```
pip3 install -r requirements.txt
```
## Database migrations.

Database migrations is managed by the ```sqlalchemy``` package ```alembic```.

First install the package into your environment with 

```pip install alembic```

After installing the alembic we need to initialize the alembic to our working project directory.

```alembic init alembic```

This will add some directories such as ```alembic``` and file ```alembic.ini```

We need to modify ```alembic.ini``` as follows

```sqlalchemy.url = postgresql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>```

Now in ```env.py``` in our alembic folder, we have to make some changes. To detect auto changes by alembic we need to give our model path to ```env.py``` as follows

```
from model import Base
target_metadata = [Base.metadata]
```

Finally, create the migration script. You can use the ```--autogenerate``` option to generate migrations based on the metadata automatically: For the first migrations we will run the following command

```alembic revision --autogenerate -m "First commit"```

Since, the migrations are already created so migrate those changes to your DB using the following command

```alembic upgrade head```

Now after any changes to the db run the above two commands to sync the changes

## How to run 

```bash
uvicorn app:app --reload
```
## Swagger Docs
Once the project is up and running go to http://127.0.0.1:8000/docs to have a working swagger documentation.