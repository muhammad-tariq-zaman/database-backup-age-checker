# database-backup-age-checker

Check each database's last backup against its RPO: BREACHED past the window, AT RISK past 80% of it, OK otherwise.

## How to run

```sh
python3 main.py backups.csv
```

## Example output

```
orders: BREACHED (last backup 36.0h ago, RPO 24h)
1 database(s) breaching RPO.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
