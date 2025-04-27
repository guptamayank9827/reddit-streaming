# Reddit Streaming

## How to run code on Docker
1. Download/Clone this repository and  `cd reddit-streaming`

2. Install Docker locally (use [Docker Desktop](https://www.docker.com/products/docker-desktop/))

3. Run `docker compose up --build` to build and run docker containers (initial setup takes a few minutes)

4. Open [localhost:5601](http://localhost:5601/) to access Kibana UI

5. Stream Data using an integration:
    1. Click on "Add Integrations"
    2. Click "Stack Management" on the side menu
    3. Click "Index Patterns" under Kibana
    4. Click "+ Create Index Pattern"
        - Name "entities*"
        - Timestamp field: @timestamp
        - Click on "Create Index Pattern"

6. Visualize data on a dashboard:
    1. Click "Dashboard" on the side menu under Analytics tab
    2. Create a new visualizaton
    3. Choose your preferred graph, preferably "Bar Vertical"
    4. On the Horizontal Axis:
        - Function: Top values
        - Field: entity.keyword
        - Number of Values: 10
        - Rank By: Entity Count
        - Rank Direction: Descending
        - Toggle off Group other values as "Other"
    5. On the Vertical Axis:
        - Function: Sum
        - Field: count
    6. Customize the date range on the top to view only for a selected time period