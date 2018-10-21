all:
	@echo "Usage:\n \044 make build \t\tTo manually build the container image"
	@echo "\t\t\tusing the docker engine\n"

	@echo "To run the demo container:"
	@echo " \044 docker run -p 5000:5000 -e APP_VERSION=v2  -e APP_MESSAGE='this message' demo-container \n"


build:
	docker build -t demo-container:latest .
