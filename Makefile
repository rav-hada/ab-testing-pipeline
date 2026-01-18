up:
	docker-compose up -d

down:
	docker-compose down

data:
	python generate_data.py

init:
	pip install -r requirements.txt

run-dbt:
	cd ab_transformation && dbt run && dbt test

check:
	python check_significance.py