# Flask Web API Sample

This project is a sample of Web API implement using [Flask](https://github.com/pallets/flask) and [Flask-Injector](https://github.com/alecthomas/flask_injector).

- APIs are written in [controllers/](./controllers/), and each API is grouped in blueprint

- The logic called by APIs are named as `XXXservice`, and on [services/](./services/)

- The `service` has an interface and implementations, and [core/application.py](./core/application.py) is configured to resolve the implementation from the interface

- However, `Python` does't have `interface` mechanism, so it uses `abstract class` instead.

- When client accesses the API, the required services are injected into the controller through arguments

# How to run it

## Setup

Quick and simply way to setup is using `pipenv`.  
[setup.sh](./setup.sh) provide you with an easier way to build environment to run it.

```bash
bash setup.sh
```

## Run

```bash
pipenv run python server.py
```

## Others

Required packages are written in [Pipfile](./Pipfile) as `[packages]`.  
Create `virtualenv` and install the packages, then you can run it.

```bash
python -m venv .venv

source .venv/bin/activate

pip install ...

python server.py
```

# Example

You can login as the built-in default user.

| username | password |
| -------- | -------- |
| admin    | admin    |
| example  | temp     |

```bash
curl -X POST http://localhost:5000/auth/jwt -H "Content-Type:application/json" -d "{\"username\": \"admin\", \"password\": \"admin\"}"
```

If the login is successful, your JWT token is returned as the response.

```json
{
  "jwt": "<Your JWT token here>"
}
```

Now you can access to the API required JWT authentication.  
As below, JWT token should be included in `Authorization` header.

```bash
curl http://localhost:5000/api/weather/jwt -H "Authorization:<Your JWT token here>"
```
