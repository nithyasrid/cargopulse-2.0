# Airflow PostgreSQL connection

The DAG expects a connection named `postgres_default`.

Create it in the Airflow UI:

- Conn Id: `postgres_default`
- Conn Type: `Postgres`
- Host: `postgres`
- Database: `cargopulse`
- Login: `cargopulse`
- Password: `cargopulse`
- Port: `5432`

For a fully automated container setup, add the connection through Airflow CLI:

```bash
docker compose exec airflow airflow connections add postgres_default \
  --conn-type postgres \
  --conn-host postgres \
  --conn-schema cargopulse \
  --conn-login cargopulse \
  --conn-password cargopulse \
  --conn-port 5432
```
