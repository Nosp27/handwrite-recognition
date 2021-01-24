# Handwrite-recognition

### Project purpose
Handwritten text recognition

### Project input data
Image submitted by user via image submit form

### Project output data
Recognized text

## Project main componenets
1. Client-side frontend: website, point of communication with user
2. Nginx: reverse-proxy + frontend server
3. Backend:
	- `Backend server`, handling requests from Client-Side page
	- `Messaging queue`, queueing heavy image processing requests
	- `Queue consumer`, reading queue and requesting ML nodes, updating status on Backend Server when predict processing finished
	- `ML Node`, serving 'predict' requests

## Usage
### Launch
```
git@github.com:Nosp27/handwrite-recognition.git && \
cd handwrite-recognition && \
docker-compose up --build
```

When launched application, open `localhost` in your browser and 
choose an image in the form. Submit the form, check out status change, 
displayed below.

### View logs

For now logs are present for ML/Message Queue and for Backend.
To view them attach to running container with help of `docker exec`
then open file in `/logs/` directory.

```
docker exec -it  docker exec -it handwrite_recognition_ml /bin/bash
more /logs/ml.log
```

Or for backend logs:
```
docker exec -it  docker exec -it handwrite_recognition_web /bin/bash
more /logs/backend.log
```

To filter logs of application itself use:
 - `grep root /logs/backend.log` for backend container
 - `grep consumer /logs/ml.log` for ml container