# player-service-python

## How to run:

1. Python 3.9 is required
2. Create a virtualenv with this cmd

```bash
python3 -m venv <path to virtual env>
# e.g.
# python3 -m venv venv
```

3. Activate virtual env

```bash
    source venv/bin/activate
```

4. Install Project dependencies

```bash
    pip install -r frf/requirements.txt
```

5. Run application

```bash
python frf/app.py
```

Now you can run the curl command or run on postman

```bash
curl http://127.0.0.1:5000/v1/players
curl http://127.0.0.1:5000/v1/players/1
```
