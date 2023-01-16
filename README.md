# Carpooling Study

A brief analysis of the behavior of a carpooling system.

## Introduction

First of all, `study.ipynb` contains the implementation of the solution described step by step.

Second, a containerized API contains a solution that stores the data in SQL and is more geared towards a production environment. The main API file is `main.py`. To run the container you need a `.env` file and then run:

```bash
docker compose build
docker compose up
```

## Repository structure

```bash
.
├── data                         # Data files
│   └── trips.csv                # Trips example data
├── db                           # Database related code
├── docker-entrypoint-initdb.d   # SQL scripts to initialize the database
├── img                          # Images for documentation
├── schemas                      # Schemas for the API
├── utils                        # Utility functions
├── loader.py                    # Facilitates data loading to SQL via API
├── main.py                      # Main API file
└── study.ipynb                  # Notebook with the step by step solution
```

## Requirements

To install the libraries needed to run `study.py` you can use [pipenv](https://pipenv.pypa.io/). The `pipenv sync` command will install everything you need.

Alternatively, a requirements.txt file is attached in case you want to install the libraries with `pip install -r requirements.txt`.

## API

### Execution

To run the API, you need to have Docker installed and position the `.env` file in the root folder (following the structure defined in `.env.example`).

Then use the following command:

```bash
docker compose build
docker compose up
```

- _**Note:** The first time containers are built there are some extra steps (such as creating the database), which can cause the API to try to communicate with MySQL before MySQL is ready. If this happens, simply stop the execution and run `docker compose up` again._

#### Initial data load

Once the API is running, the first step will surely be to load the data. Since the API receives information in JSON format and the original data is in CSV, `loader.py` has been implemented to make it faster to load data from a CSV file. To use it, just run:

```bash
python loader.py
```

By default, `loader.py` use `data/trips.csv` as the CSV file to load, but if you want to use another file, you can do it by running:

```bash
python loader.py [csv_filename]
```

### Endpoints

API endpoints are documented with [Swagger](https://swagger.io/tools/swagger-ui/) and, once the container is running, can be reviewed at [localhost:8000/docs](http://localhost:8000/docs). Here is a summary of the endpoints:

- `GET /ping`: Checks if the API is running
- `GET /data`: Returns the data stored in the database
- `POST /data`: Loads data to the database
- `GET /carpooling`: Calculate the carpooling based on actual stored data
- `GET /average-weekly-trips`: Calculate the average weekly trips based on actual stored data given a bounding box and region.
