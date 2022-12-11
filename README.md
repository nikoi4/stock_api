# Stock Market API Service Challenge

Background: refer to [challenge doc](https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md)

## Considerations
* DB as sqlite as plug and play db suitable for the purpose of this project
* Django settings in one file but it should go into sepparate files each for its respective environment
* Basic AWS EC2 config (free tier) only to host the project

## API

### Endpoints

* `POST /api/v1/register/`

Request schema:
```json
"actions": {
    "POST": {
        "username": {
            "type": "string",
            "required": true,
            "read_only": false,
            "max_length": 150
        },
        "email": {
            "type": "email",
            "required": false,
            "read_only": false,
            "max_length": 254
        },
        "first_name": {
            "type": "string",
            "required": false,
            "read_only": false,
            "max_length": 150
        },
        "last_name": {
            "type": "string",
            "required": false,
            "read_only": false,
            "max_length": 150
        },
        "password": {
            "type": "string",
            "required": true,
            "read_only": false,
            "max_length": 128
        }
    }
}
```
Response schema:
```json
{"token": "string"}
```

* `POST /api/v1/api-token-auth/`

Request schema:
```json
"actions": {
    "POST": {
        "username": {
            "type": "string",
            "required": true,
            "read_only": false,
            "max_length": 150
        },
        "password": {
            "type": "string",
            "required": true,
            "read_only": false,
            "max_length": 128
        }
    }
}
```
Response schema:
```json
{"token": "string"}
```

* `GET /api/v1/stock_info/<stock_symbol>`
`Header --> 'Authorization: Token <token from register/ or api-token-auth/>'`

Request schema:
```json
"actions": {
    "GET": {
        "stock_symbol": {
            "type": "string",
            "required": true,
        }
    }
}
```
Response schema:
```json
{
    "open_price": string,
    "higher_price": string,
    "lower_price": string,
    "variation": string,
}
```

## Run api

### Local dev

#### Requirements
* Clone repo
* python 3.10.6
* venv
* dependencies
* DJANGO_SECRET_KEY and ALPHAVANTAGE_API_TOKEN must be exported

#### Steps:
1. Step into repo and run `python3 -m venv venv`
2. Activate venv by `source venv/bin/activate`
3. Install requirements by `pip install -r requirements.txt
4. Create an .env file and export DJANGO_SECRET_KEY=(copy result of running openssl rand -base64 32) and ALPHAVANTAGE_API_TOKEN=(get it from https://www.alphavantage.co/support/#api-key)
5. Source .env file `source .env`
6. Make and run migrations `python eureka_stock_api/manage.py makemigrations && python eureka_stock_api/manage.py migrate`
6. Run django server `python eureka_stock_api/manage.py runserver 8080`
7. With any request tool like curl make calls using http://localhost:8080<api endpoint>

### Local Docker

#### Requirements
* Docker
* DJANGO_SECRET_KEY and ALPHAVANTAGE_API_TOKEN must be exported

#### Steps:
1. Step into repo and run `docker build -t eureka_stock_api:latest .`
2. Create an .env file and export DJANGO_SECRET_KEY=(copy result of running openssl rand -base64 32) and ALPHAVANTAGE_API_TOKEN=(get it from https://www.alphavantage.co/support/#api-key)
3. Source .env file `source .env`
4. Create and run container `docker run --name eureka_stock_api -e ALPHAVANTAGE_API_TOKEN=$ALPHAVANTAGE_API_TOKEN -e DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY -p 8000:8000 eureka_stock_api:latest`
5. With any request tool like curl make calls using http://0.0.0.0:8000<api endpoint>

### AWS
With any request tool like curl make calls using `http://ec2-54-152-250-81.compute-1.amazonaws.com:8000<api endpoint>`

### Testing

#### Runing unit tests in local dev
##### Steps
1. Same as local dev steps 1 to 5
2. `pytest`

#### Running testing client
##### Steps
1. Same as local dev steps 1 to 6
2. In another terminal tab or window repeat 1 to 3
3. Run client `python client/main.py`
