# Step 1 — Payment Request Queue
import queue

payment_queue = queue.Queue()

def add_payment_request(user_id, amount):
    request = {
        "user_id": user_id,
        "amount": amount
    }

    payment_queue.put(request)
    print("Payment request added to queue:", request)


# Step 2 — Worker Processing
import threading
import time
import requests

PAYMENT_API_URL = "https://third-party-payment.com/pay"

def payment_worker():

    while True:

        request = payment_queue.get()

        try:
            response = requests.post(
                PAYMENT_API_URL,
                json=request,
                timeout=5
            )

            print("Payment processed:", response.status_code)

        except Exception as e:
            print("Payment failed:", e)

        payment_queue.task_done()

        time.sleep(0.1)  # simple rate limit


# Step 3 — Start Workers
for _ in range(5):  # 5 workers
    t = threading.Thread(target=payment_worker)
    t.daemon = True
    t.start()

# Now only 5 payment requests will run in parallel, protecting the payment service.

# Step 4 — Simulating Traffic Spike

for i in range(100):
    add_payment_request(user_id=i, amount=100)

# Result:
'''
100 requests go into the queue
Workers process them gradually
Payment API is not overloaded
Production Architecture (Real Systems)

In production systems:
    Queue
    Redis
    RabbitMQ
    Kafka
    AWS SQS

Workers
    Celery workers
    Kubernetes workers

Monitoring
    Prometheus
    Grafana

Short Interview Answer (30 seconds)

You can say:
    If payment requests spike, I would not call the third-party payment API directly. 
    Instead, I would introduce a message queue between the API server and the payment service. 
    Incoming payment requests are pushed into the queue, 
    and background workers process them at a controlled rate. 
    This prevents overloading the payment service. I would also implement rate limiting, 
    retries with exponential backoff, and idempotency keys to ensure reliable and safe payment processing.
'''