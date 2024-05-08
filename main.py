from modules.utils import env
import prometheus_client as prom
from modules.tim_client import TimModemAPI
from http.server import HTTPServer, BaseHTTPRequestHandler

tim = TimModemAPI(
    router_ip=env.ROUTER_IP,
    username=env.ADMIN_USERNAME,
    password=env.ADMIN_PASSWORD
)
tim.login()

metrics = {
    "internet_down": prom.Counter(
        f"{env.PROMETHEUS_PREFIX}_internet_download_bytes_total",
        "Internet download bytes"
    ),
    "internet_up": prom.Counter(
        f"{env.PROMETHEUS_PREFIX}_internet_upload_bytes_total",
        "Internet upload bytes"
    )
}


def update_metrics():
    down_delta, up_delta = tim.get_internet_delta()
    metrics["internet_down"].inc(down_delta)
    metrics["internet_up"].inc(up_delta)


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            update_metrics()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(prom.generate_latest())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


if __name__ == "__main__":
    prom.disable_created_metrics()
    prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    prom.REGISTRY.unregister(prom.GC_COLLECTOR)

    server = HTTPServer(("0.0.0.0", env.PROMETHEUS_PORT), MetricsHandler)
    server.serve_forever()
