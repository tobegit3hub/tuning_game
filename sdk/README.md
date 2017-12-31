# Tuning Game SDK

## Installation

```
pip install tuninggame
```

## Usage

Find more code in [examples](./examples).

```
# Create client
endpoint = "http://0.0.0.0:8000"
client = TuningGameClient(endpoint)

# Create competition
competition = client.create_competition("TestCompetition", {}, "MAXIMIZE", 100)

# Create participation
participation = client.create_participation(competition.id, "TestUser", "test@gmail.com")

# List trials
trials = client.list_trials()

# Create trial
trial = client.create_trial(participation.id, {"parameter": 10.0})

# Get trial
get_trial = client.get_trial_by_id(trial.id)

# Delete trial
client.delete_trial(get_trial.id)

# Delete participation
client.delete_participation(participation.id)

# Delete competition
client.delete_competition(competition.id)
```

## Deployment

```
python setup.py sdist --format=gztar

twine upload dist/tuninggame-x.x.x.tar.gz
```
