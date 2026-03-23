
# Containers

This section contains all the containers required to emulate a real infrastructure

## Folder Structure

```bash
.containers
├── broker/
├── cache/
├── database/
├── logs/
├── metrics/
├── provider/
├── traces/
├── vizualization/
├── docker-compose.observability.yaml
└── README.md
```

## Archtecture

```mermaid
  graph TD
    subgraph DockerEngine
      application["Application"]
      database["Database"]
      broker["Message Broker"]
      cache["Cache"]
      localstack["LocalStack"]

      subgraph Observability
        promtail["Promtail"]
        prometheus["Prometheus"]
        otel["OTel Collector"]
        mimir["Mimir"]
        loki["Loki"]
        tempo["Tempo"]
      end

      subgraph Vizualization
        grafana["Grafana"]
        pmm["PMM"]
        insights["Redis Insights"]
        redpanda["Redpanda"]
      end

    end

    application <-->|connect| database
    application <-->|connect| cache
    application <-->|produce/consume| broker
    application <-->|connect| localstack
    application -->|scrape| prometheus
    application -->|scrape| promtail
    application -->|push| otel
    prometheus -->|push| mimir
    promtail -->|push| loki
    otel -->|push| tempo
    mimir -->|connect| grafana
    tempo -->|connect| grafana
    loki -->|connect| grafana
    database -->|connect| pmm
    cache -->|connect| insights
    broker -->|connect| redpanda
```

### Logs

application -writes-> stdout <-scrape- promtail -pushes-> loki

### Metrics

application <-scrapes- prometheus -pushes-> mimir


[Local Prometheus](http://localhost:9090)


### Traces

application -pushes-> otel-collector -pushes-> tempo

### Vizualization

[Local Grafana](http://localhost:3000)
