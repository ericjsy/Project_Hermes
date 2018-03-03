# Welcome to datatracker!

**Requirements:** Python 3.5, PostgreSQL 9.5.3  
**Recommended clients:** PyCharm, PGAdmin III  

Install appropriate packages:

```
pip install -r requirements.txt
```

Update database.ini file:

```
[postgresql]
host=
database=
user=
password=
port=
```

Create database:

```
createdb -h 127.0.0.1 -p 5432 -U postgres -W datatracker
```

Create superuser:

```
createuser -h 127.0.0.1 -p 5432 -U postgres -P -s -e dt_admin
```

Set up database:

```
psql -h 127.0.0.1 -f db_setup.sql -d datatracker postgres
```

Run datatracker program (cmd):

```
python main.py
```


