# Reddit Streaming

## How to run code on Docker
1. Download/Clone this repository and  `cd reddit-streaming`

2. Install Docker locally (use [Docker Desktop](https://www.docker.com/products/docker-desktop/))

3. Run `docker compose up --build` to build and run docker containers (initial setup takes a few minutes)

4. Open [localhost:5601](http://localhost:5601/) to access Kibana UI

5. Stream Data using an integration:
    - Click on "Add Integrations"
    - Click "Stack Management" on the side menu
    - Click "Index Patterns" under Kibana
    - Click "+ Create Index Pattern"
        1. Name "entities*"
        2. Timestamp field: @timestamp
        3. Click on "Create Index Pattern"