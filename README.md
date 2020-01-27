## Setup project

1. Install `docker` and `docker-compose`
1. Rename `default.env` file to `.env`
1. Set environment variable in `.env` file
1. Setup project via `make setup_project`
1. Create migrations via `docker-compose run --rm liquibase update`

## Run project

Run via `make run_project`

## Run psql

Run via `make run_psql`


## Create a migration on DB schema change

1. Add new changeSet to server/migrations with semantic name like "001_create_user_table.xml"
1. Create change via `docker-compose run --rm liquibase update` 


## Rollback a migration

Rollback by count migrations via `docker-compose run --rm liquibase rollbackCount <count>`
###### or

Rollback by date migrations via `docker-compose run --rm liquibase rollbackToDate <yyyy-MM-dd'T'HH:mm:ss>`

## Run tests

Run via `make run_tests`
