import os


class EnvironmentConfig:
    def __init__(self):
        self.PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "8000"))
        self.PROMETHEUS_PREFIX = os.getenv("PROMETHEUS_PREFIX", "tim")
        self.ROUTER_IP = os.getenv("ROUTER_IP", "192.168.1.1")
        self.ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Administrator")
        self.ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


env = EnvironmentConfig()
