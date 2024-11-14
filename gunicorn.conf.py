import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:5000"
timeout = 300
worker_class = 'gthread'
threads = 4
max_requests = 1000
max_requests_jitter = 50 