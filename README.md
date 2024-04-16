systemctl daemon-reload

-- socket
sudo nano /etc/systemd/system/gunicorn-dev.socket

[Unit]
Description=gunicorn dev socket
[Socket]
ListenStream=/run/gunicorn-dev.sock
[Install]
WantedBy=sockets.target

-- service
sudo nano /etc/systemd/system/gunicorn-dev.service

[Unit]
Description=gunicorn dev daemon
Requires=gunicorn-dev.socket
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/web_app/

ExecStart=/root/web_app/webapp/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn-dev.sock \
         webapp.webapp.wsgi:application
[Install]
WantedBy=multi-user.target


--nginx
sudo nano /etc/nginx/sites-available/api_dev
sudo ln -s /etc/nginx/sites-available/api_dev /etc/nginx/sites-enabled/api_dev
                                                            
server {
        server_name www.freshautoshop.ru freshautoshop.ru;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
                root /root/web_app/;
        }
        location /media/ {
                root /root/web_app/;
        }
        location / {
                include proxy_params;
                proxy_pass http://unix:/run/gunicorn.sock;
        }
} 







