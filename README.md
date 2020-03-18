# ABC-SERVER

Server boilerplate to gain sings from people.

## Project deploy
You need: 
- nginx with ngx_http_memcached_module
- memcached
- wsgi server
- postgres database server

Idea is to cache slow queries with memcached. App puts data to memcached,
nginx get em from there.

## Project setup
1. Create postgres database and run create.sql within.
2. Edit config.py to match you services addresses.
3. Run pip install -r requirements.txt
4. Run wsgi under nginx.

If you will run client and server on same port remove CORS to make app lighter. 

Cheers!