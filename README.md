# Initial setup
## Dependencies
- sqlite3
- memcached
- python3
- pip
- curl

```bash
virtualenv -p python3 env

source ./env/bin/activate

pip install -r requirements.txt

python manage.py migrate
```

## Make sure memcache is running
I'm using a macbook, in which case:

```bash
brew install memcached

brew services run memcached
```

# To download the files
```bash
./generate_files.sh
```

# To run tests
```bash
./run_tests.sh
```
