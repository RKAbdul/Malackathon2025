bind = "0.0.0.0:443"
keyfile = "/home/ubuntu/malackathon/certs/malackathon.app.key"
certfile = "/home/ubuntu/malackathon/certs/fullchain.crt"

workers = 10               # start with 2; tune = 2-4 * vCPU
threads = 20               # good for I/O-heavy apps like Dash
timeout = 120
keepalive = 30
graceful_timeout = 30
preload_app = True        # faster worker start, lower RAM if imports are large

accesslog = "/home/ubuntu/malackathon/logs/access.log"
errorlog  = "/home/ubuntu/malackathon/logs/error.log"
loglevel = "info"