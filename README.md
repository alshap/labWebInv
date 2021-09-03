# Inventory web app(Django)

Run instructions:

1. Download source

2. Open project folder

3. Get setting.py file

4. Specify static files dir and database in setting.py

5. Migrate database change with cmd

```
python3 manage.py makemigrations
python3 manage.py migrate
```

6. Restore database from dump

On Windows cmd
```
./psql.exe -U postgres -d <dbname> -f <psqlpath>
```

7. Run server

Local
```
python3 manage.py runserver
```
Public
```
python3 manage.py runserver '0.0.0.0:8000'
```

