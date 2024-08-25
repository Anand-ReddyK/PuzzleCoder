# PuzzleCoders

## Prerequisites
1. **Docker**
2. **MongoDB**

## Setup Instructions

Clone the repository
```
git clone https://github.com/Anand-ReddyK/Real-Time-Chat-App.git
```

  
Build the images

for Linux run
```
chmod +x build-images.sh
./build-images.sh
```

for Windows open PowerShell and run
```
.\build-images.ps1
```

Initialize Docker Swarm
```
docker swarm init
```

Deploy the application using Docker Stack with the `docker-compose.yml` file
```
docker stack deploy -c docker-compose.yml puzzlecoder
```
now you can access the application at `http://127.0.0.1:8000/`

To stop and remove the application stack, use
```
docker stack rm puzzlecoder
```
