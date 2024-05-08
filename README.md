# tim-technicolor-exporter
A very crude Prometheus exporter that exports some stats for a particular type of router made by TIM Technicolor.  
**It will very likely not work with any other type/model/brand of router**, I just made this primarily for myself.

## Usage
The exporter is configured using environment variables.  
Every variable has a default value except for the Admin interface password, for obvious reasons.

| Variable            | Description                           | Default           |
|---------------------|---------------------------------------|-------------------|
| `PROMETHEUS_PORT`   | The port the exporter listens on      | `8000`            |
| `PROMETHEUS_PREFIX` | The prefix for the Prometheus metrics | `"tim"`           |
| `ROUTER_IP`         | The IP address of your router         | `"192.168.1.1"`   |
| `ADMIN_USERNAME`    | The username for the web interface    | `"Administrator"` |
| `ADMIN_PASSWORD`    | The password for the web interface    | -                 |

## Docker
The exporter is available as a Docker image on the [GitHub Container Registry](https://ghcr.io/pesaventofilippo/tim-technicolor-exporter).

To run the exporter using Docker, you can use the following command:
```bash
docker run -d -p 8000:8000 \
    -e ADMIN_PASSWORD="YOUR_PASSWORD" \
    ghcr.io/pesaventofilippo/tim-technicolor-exporter
```

### docker-compose
You can also use `docker-compose` to run the exporter.
Here is an example `docker-compose.yml` file:
```yaml
services:
  nut-exporter:
    image: ghcr.io/pesaventofilippo/tim-technicolor-exporter
    ports:
      - 8000:8000
    environment:
      ADMIN_PASSWORD: YOUR_PASSWORD
```
