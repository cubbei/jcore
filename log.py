from datetime import datetime



def debug(message: str):
    print(f"{datetime.now()} DBG: {message}")

def log(message: str):
    print(f"{datetime.now()} LOG: {message}")

def info(message: str):
    print(f"{datetime.now()} INF: {message}")

def warning(message: str):
    print(f"{datetime.now()} WRN: {message}")

def critical(message: str):
    print(f"{datetime.now()} CRT: {message}")