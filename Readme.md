### build and run 
docker-compose up -d --build 

### Swagger docs are now available here
http://0.0.0.0:8101/api/v1/docs






# Urls 

postgres://merlin_user:123456@localhost:54329/merlin_recognizer_database
postgres://merlin_user:123456@postgres-db:5432/merlin_recognizer_database

### Migrations 
Generate migrations 
```
 $ PYTHONPATH=. alembic revision --autogenerate -m "comment"
 $ PYTHONPATH=. alembic upgrade head
```
### 


