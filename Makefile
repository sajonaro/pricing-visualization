
kill:
	@CONTAINER_ID=$$(docker ps | grep 'widget' | cut -d ' ' -f 1); \
	echo "Killing container with ID: $$CONTAINER_ID";\
	docker kill $$CONTAINER_ID 
		
	
run:
	docker build -t widget . --no-cache ;\
	docker run -p 8501:8501 widget 