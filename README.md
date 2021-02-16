# Trade Stats

```shell
sudo nano /etc/systemd/system/gunicorn.service
```
```editorconfig
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/tradestats-django
ExecStart=/home/ubuntu/tradestats-django/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/tradestats-django/tradestats.sock tradestats.wsgi:application

[Install]
WantedBy=multi-user.target

```
```shell
sudo nano /etc/nginx/sites-available/tradestats
```

```
server {
    listen 80;
    server_name 206.189.133.46;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/tradestats-django;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/tradestats-django/tradestats.sock;
    }
}

```
```shell
crontab -e
```
```
15 03 * * * /home/ubuntu/tradestats-django/venv/bin/python /home/ubuntu/tradestats-django/manage.py fetch_instrument_masters
```