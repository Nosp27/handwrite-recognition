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
