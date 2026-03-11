# Remote Deployment

This project is a `FastAPI` service and is suitable for deployment with `systemd + nginx` on an Ubuntu server.

## 1. Prepare the server

Install system packages:

```bash
sudo apt update
sudo apt install -y nginx git curl
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

If PostgreSQL is hosted on another machine, make sure the server can reach the database host and port.

## 2. Upload the project

Clone or copy the repository to `/opt/captive_portal`:

```bash
sudo mkdir -p /opt/captive_portal
sudo chown -R $USER:$USER /opt/captive_portal
git clone <your-repo-url> /opt/captive_portal
cd /opt/captive_portal
```

## 3. Create the Python environment with uv

```bash
uv python install 3.11
uv venv --python 3.11
uv sync --frozen
```

## 4. Configure application settings

Edit `src/configs/site_settings.py` on the server:

```bash
nano /opt/captive_portal/src/configs/site_settings.py
```

Recommended production content:

```python
APP_HOST = "0.0.0.0"
PORT = 8000
DEBUG = False
DB_URI_OTC = "postgresql+psycopg2://USER:PASSWORD@DB_HOST:5432/captive_portal"
```

## 5. Run database migrations

```bash
cd /opt/captive_portal/src
../.venv/bin/python -m alembic upgrade head
```

## 6. Install the systemd service

The provided unit file assumes the project path is `/opt/captive_portal` and the Linux user is `ubuntu`.

If your server uses another account, update `User=` and `Group=` in `deploy/systemd/captive-portal.service` before installing it.

```bash
sudo cp /opt/captive_portal/deploy/systemd/captive-portal.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable captive-portal
sudo systemctl start captive-portal
sudo systemctl status captive-portal
```

View logs:

```bash
sudo journalctl -u captive-portal -f
```

## 7. Install the nginx config

```bash
sudo cp /opt/captive_portal/deploy/nginx/captive-portal.conf /etc/nginx/sites-available/captive-portal
sudo ln -sf /etc/nginx/sites-available/captive-portal /etc/nginx/sites-enabled/captive-portal
sudo nginx -t
sudo systemctl reload nginx
```

## 8. Open firewall ports

If `ufw` is enabled:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## 9. Optional: enable HTTPS

If you have a domain name already pointing to the server:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d <your-domain>
```

## Notes

- Runtime settings are loaded from `src/configs/site_settings.py`.
- `APP_HOST`, `PORT`, `DEBUG`, and `DB_URI_OTC` can all be configured there.
- Python 3.11 and the `.venv` directory are both managed by `uv`.
- The service still starts `/opt/captive_portal/.venv/bin/python`, but that interpreter comes from the `uv`-managed virtual environment.
- If you want, this can also be packaged into a `Dockerfile` and `docker-compose.yml`.
