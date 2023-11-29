recreate: 
	docker remove project-template-generator-llm-backend-1
	docker rmi project-template-generator-llm-backend
	docker-compose up

.PHONY : recreate