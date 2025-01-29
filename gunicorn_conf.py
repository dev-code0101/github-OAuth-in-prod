bind = "0.0.0.0:8000"
workers = 3  # Adjust based on server CPU (2 for t2.micro)
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120


# gunicorn -c gunicorn_conf.py app.main:app
