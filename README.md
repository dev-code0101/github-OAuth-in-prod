```
GitHub Repo → Settings → Secrets → Actions:
Secret Name Value (Example)
DOCKER_USERNAME your_dockerhub_username
DOCKER_PASSWORD your_dockerhub_password
SERVER_HOST your_server_ip (e.g., 192.168.1.1)
SERVER_USER your_ssh_username (e.g., ubuntu)
SERVER_PASSWORD your_ssh_password
```

```bash
chmod +x setup.sh
./setup.sh
```

```bash
chmod +x deploy.sh
./deploy.sh
```
