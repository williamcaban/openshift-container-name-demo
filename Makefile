all:
	@echo "Usage:\n \044 make build \t\tTo manually build the container image"
	@echo "\t\t\tusing the docker engine\n"

	@echo "To run the demo container:"
	@echo " \044 docker run -p 5000:5000 demo-container \n"
	@echo " \044 docker run -p 5000:5000 -e APP_VERSION=v2  -e APP_MESSAGE='Demo message' demo-container \n"

	@echo "To test the application point a local browser to http://localhost:5000 or use the 'curl' command:"
	@echo " \044 while sleep 1; do curl http://localhost:5000/hello; echo; done \n\n"

build:
	docker build -t demo-container:latest .
