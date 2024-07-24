# Payments app
## Running with docker-compose
- Create `.env` file and copypaste into it:
```
MYSQL_ROOT_PASSWORD: rootpass
MYSQL_DATABASE: mydb
DB_HOST=db 
DJANGO_SECRET_KEY=your_secret_key_that_shouldnt_be_committed_anywhere
```
DB_HOST should match the mysql service name in docker-compose file.

Better not to use root user in prod, create another user and grant him necessary privileges.
- `make compose_up` to run
- Open http://0.0.0.0:8000/api/ in browser. You can add wallets or transactions, and navigate through them.
- `make compose_down` to stop

## Running tests
- `pip install -r requirements.txt`
- `pip install -r requirements_test.txt`
- `pytest`