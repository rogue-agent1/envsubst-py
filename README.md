# envsubst-py
Substitute `$VAR` and `${VAR}` in files using environment variables.
```bash
echo "Hello $USER at $HOME" | python envsubst.py
python envsubst.py template.conf -o output.conf --env-file .env
python envsubst.py config.yaml -e "DB_HOST=localhost" "DB_PORT=5432"
```
## Zero dependencies. Python 3.6+.
