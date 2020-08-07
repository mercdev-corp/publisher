# Publisher

Bootsrap project to publush content via admin and fetch it via API. Order of attached content can be changed in admin using `order` field.

Admin access via `/admin/`:

```
username: admin
password: adMIN1234
```

can be changed via `daphne` and `runserver` services environment variables `docker-compose.yml`

## Execution

`docker-compose up runserver` will execute required containers (postgres, rabbitmq, celery) and project itself with `manage.py runserver 0.0.0.0:8000` command.

`docker-compose up runserver` will execute required containers (postgres, rabbitmq) and django tests with `manage.py test --noinput` command. Project container will be stopped at process end.

`docker-compose up web` will execute requred containers (postgres, rabbitmq, celery, daphne, nginx) to run project in production-like mode with daphne application server and serving static via nginx. Use 0.0.0.0:80 for access.

## API

### `/api/v1/page/list/`

`GET` - return paginated list of pages with titles, id and url to API endpoint to fetch detailed info.

**Example**

```json
{
   "count":1,
   "next":null,
   "previous":null,
   "results":[
      {
         "id":11,
         "title":"First page",
         "details_url":"/api/v1/page/11/"
      }
   ]
}
```

### `/api/v1/page/<ID>/`

`GET` - return detailed information about target page and attached content. Including info about those content.

**Example**

```json
{
   "id":11,
   "texts":[
      {
         "id":22,
         "title":"Other text",
         "original_text":"Other text content",
         "counter":1
      },
      {
         "id":21,
         "title":"Some text",
         "original_text":"Text content",
         "counter":1
      }
   ],
   "audios":[
      {
         "id":1,
         "title":"Bauchamp",
         "bitrate":256,
         "url":"/media/uploads/content/11/Audio/Author-Track.mp3",
         "counter":1
      }
   ],
   "videos":[
      {
         "id":1,
         "title":"Video",
         "subtitles":"",
         "url":"https://www.youtube.com/watch?v=XXXXXXXX",
         "counter":1
      }
   ],
   "title":"First page"
}
```
