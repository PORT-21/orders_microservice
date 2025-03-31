generate_client_lib:
	openapi-python-client generate --path ./openapi.json


build:
	docker build . -t 10.8.0.12/<REPO>:latest


push:
	docker push 10.8.0.12/<REPO>:latest


deliver:
	docker build . -t 10.8.0.12/<REPO>:latest && docker push 10.8.0.12/<REPO>:latest
