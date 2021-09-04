# PromSQL: PromQL on top of SQL

This project implements the PromQL lamguage on top of SQL databases in order to  query them with a timeseries query language. This way, we can query already existing data in SQL databases as if they are stored in a timeseries database like Prometheus.

Tasks:

- [x] Implement the PromQL grammar in LARK
- [x] Implement fetching data from the SQL database using sqlalchemy
- [ ] Implement all nodes
- [ ] Implement config manager

## How to use?

First run the docker-compose file:
```bash
docker-compose up
```

Then push some data in the QuestDB database using  

```bash
pip install -r requirements.txt
pip install -e .
promsql-cli.py
```

Then in the opened command prompt, enter the following:

```bash
promsql > telemetry[5m]
```

This will get all the telemety metric values since the last 5 minitues.

## How to change the configs
Right now, the only way to change the configs is changing the values in the `promsql/constants.py` file. 