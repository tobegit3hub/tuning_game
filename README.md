# Tuning Game

## Introduction

The hyper-parameters tuning game for black box optimization

## Usage



## Deploy

```
./manage.py makemigrations tuning
./manage.py migrate
./manage.py initialize_database
./manage.py runserver 0.0.0.0:8000
```

## Test

Run the unit tests.

```
./manage.py test --pattern="*_test.py"
```
