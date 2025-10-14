# Testing RPS

```bash
# check limits
ulimit -n
ulimit -n 65535
```

```bash
wrk -t12 -c400 -d30s http://localhost:8000/
```

## `CMD ["/bin/bash"]`

```bash
Running 30s test @ http://localhost:8000/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    75.89ms  230.12ms   1.66s    94.63%
    Req/Sec   812.81    448.48     2.02k    62.26%
  261321 requests in 30.06s, 31.15MB read
  Socket errors: connect 157, read 0, write 0, timeout 0
Requests/sec:   8692.34
Transfer/sec:      1.04MB
```

## `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`

```bash
Running 30s test @ http://localhost:8000/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    46.26ms   79.19ms   1.99s    98.19%
    Req/Sec   487.82    228.85     1.86k    71.15%
  174614 requests in 30.05s, 20.82MB read
  Socket errors: connect 157, read 0, write 0, timeout 42
Requests/sec:   5811.28
Transfer/sec:    709.38KB
```

## `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]`

```bash
Running 30s test @ http://localhost:8000/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    46.70ms   81.82ms   1.99s    98.33%
    Req/Sec   493.30    206.95     1.43k    69.59%
  176087 requests in 30.05s, 20.99MB read
  Socket errors: connect 157, read 0, write 0, timeout 28
Requests/sec:   5860.66
Transfer/sec:    715.41KB
```

Почти индентичны предыдущему

## `CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]`

```bash
Running 30s test @ http://localhost:8000/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    49.78ms   88.40ms   2.00s    98.26%
    Req/Sec   463.05    225.51     1.39k    70.38%
  164781 requests in 30.03s, 19.64MB read
  Socket errors: connect 157, read 0, write 0, timeout 36
Requests/sec:   5487.27
Transfer/sec:    669.83KB
```

## `CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]`

```bash
Running 30s test @ http://localhost:8000/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    66.90ms   78.91ms   1.98s    98.65%
    Req/Sec   505.05    167.63     1.70k    67.39%
  180509 requests in 30.05s, 21.52MB read
  Socket errors: connect 0, read 0, write 0, timeout 186
Requests/sec:   6006.76
Transfer/sec:    733.25KB
```
