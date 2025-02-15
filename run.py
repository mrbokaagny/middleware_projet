import multiprocessing
import os

def run_app():
    os.system("python app/app.py")

def run_middleware():
    os.system("python middleware/middleware.py")

def run_users():
    os.system("python services/user/app.py")

def run_products():
    os.system("python services/product/app.py")

if __name__ == "__main__":
    processes = []

    for func in [run_middleware, run_users, run_products, run_app]:
        p = multiprocessing.Process(target=func)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
