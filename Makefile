include .env
export

setup_project:
		docker-compose up -d database
		docker-compose up -d camunda
		curl -w "\n" \
            -H "Accept: application/json" \
            -F "deployment-name=BetAggr" \
            -F "enable-duplicate-filtering=true" \
            -F "deploy-changed-only=true" \
            -F "betaggr.bpmn=@betaggr.bpmn" \
            http://$(CAMUNDA_API_HOST):$(CAMUNDA_API_PORT)/engine-rest/deployment/create
		docker-compose build
run_project:
		docker-compose up server
run_psql:
		docker-compose run --rm database psql -U $(POSTGRES_DB) -h $(POSTGRES_HOST)
run_tests:
		docker-compose -f docker-compose.testing.yml up -d test_database
		docker-compose -f docker-compose.testing.yml up -d camunda
		docker-compose -f docker-compose.testing.yml build
		curl -w "\n" \
            -H "Accept: application/json" \
            -F "deployment-name=BetAggr" \
            -F "enable-duplicate-filtering=true" \
            -F "deploy-changed-only=true" \
            -F "betaggr.bpmn=@betaggr.bpmn" \
         http://$(CAMUNDA_API_HOST):$(CAMUNDA_API_PORT)/engine-rest/deployment/create
		docker-compose -f docker-compose.testing.yml run --rm test_server
		docker-compose -f docker-compose.testing.yml down
