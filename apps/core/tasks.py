from rede_gsti.celery import app


@app.task
def testing_async():
    print('Tah async mano!')