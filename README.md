# Django Deployment with Gunicorn and Nginx

This guide explains how to deploy a Django application using Gunicorn as the application server and Nginx as a reverse proxy.

## Prerequisites

- A server with a Linux-based operating system (Ubuntu recommended).
- Python 3 installed on the server.
- Basic understanding of command-line operations.

---

## Installation Steps

### 1. Install Required Packages

Update the server's package index and install Python, pip, and Nginx:

```bash
sudo apt update
sudo apt install python3-pip python3-dev nginx
2. Install Django and Gunicorn
Install Django and Gunicorn using pip:


pip install django gunicorn
Create a Django project:


django-admin startproject your_project_name
3. Allow Port 8000 in Firewall
Enable traffic on port 8000 for testing:

sudo ufw allow 8000
Run the application to ensure it's working locally:


~/projectdir/manage.py runserver 0.0.0.0:8000
If the application runs successfully, proceed to configure Gunicorn.

4. Configure Gunicorn
Start Gunicorn for Testing
Run Gunicorn to serve the Django application:


gunicorn --bind 0.0.0.0:8000 your_project_name.wsgi
Create a Gunicorn Socket File
Create a socket file to manage Gunicorn:


sudo vim /etc/systemd/system/gunicorn.socket
Add the following content:

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
Create a Gunicorn Service File
Create a service file to manage Gunicorn:


sudo vim /etc/systemd/system/gunicorn.service
Add the following content (replace torjo and projectdir with your username and project directory):


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
          your_project_name.wsgi:application

[Install]
WantedBy=multi-user.target
5. Configure Nginx as a Reverse Proxy
Create an Nginx configuration file for your project:


sudo vim /etc/nginx/sites-available/your_project_name
Add the following configuration:

nginx
Copy code
server {
    listen 80;
    server_name localhost;
    
    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/torjo/projectdir/your_project_name;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
Activate the configuration by creating a symbolic link:


sudo ln -s /etc/nginx/sites-available/your_project_name /etc/nginx/sites-enabled/
Restart Nginx to apply the changes:


sudo systemctl restart nginx
6. Starting the Services
Enable and start Gunicorn and Nginx:


sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
Directory Structure
The directory structure for your project should look like this:


/home/torjo/projectdir/
├── your_project_name/
│   ├── your_project_name/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── static/
├── env/  # Virtual environment directory
└── requirements.txt
