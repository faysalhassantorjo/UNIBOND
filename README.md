Deploy this proejct using NGINX web server


Installing python and nginx

update the server's package index 
sudo apt update
sudo apt install python3-pip python3-dev nginx


This will install python, pip and nginx server

Installing Django and gunicorn

pip install django gunicorn
Create a Python Application
Django-admin startprojct your_project_name



sudo ufw allow 8000


This opens port 8000 by allowing it over the firewall.


Check that the is project open on 8000 port
~/projectdir/manage.py runserver 0.0.0.0:8000


If Application Run successfully on local server then Configure the Gunicorn



Configuring Gunicorn

gunicorn's ability to serve our application by firing the following commands:
gunicorn --bind 0.0.0.0:8000 unibond.wsgi

Let's create a system socket file for gunicorn now:
sudo vim /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target


























Next, we will create a service file for gunicorn
sudo vim /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=torjo
Group=www-data
WorkingDirectory=/home/torjo/projectdir
ExecStart=/home/torjo/projectdir/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          studybud.studybud.wsgi:application

[Install]
WantedBy=multi-ser.target












Configuring Nginx as a reverse proxy


sudo vim /etc/nginx/sites-available/unibond

server {
    listen 80;
    server_name localhost;       
    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/torjo/projectdir/studybud;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

Activate the configuration using the following command 

sudo ln -s /etc/nginx/sites-available/unibond /etc/nginx/sites-enabled/



Restart nginx and allow the changes to take place.
sudo systemctl restart nginx
