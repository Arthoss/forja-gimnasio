# FORJA — Proyecto Django (Gimnasio)

Proyecto académico desarrollado con Django. Incluye dos apps (`gimnasio` y `ejercicios`) y consume dos microservicios externos:

- Uno de terceros (`api.quotable.io`) para frases motivacionales.
- Uno propio, construido para esta actividad, que consulta una base de datos en la nube.

## Apps del proyecto

- **gimnasio**: clases, inscripciones y frase motivacional del día.
- **ejercicios**: catálogo de ejercicios organizado por categoría, con filtro por nivel.

## Vistas destacadas

- `gimnasio.views.detail` y `gimnasio.views.inscribirse` usan `get_object_or_404()` para devolver un 404 controlado si la clase no existe.
- `gimnasio.views.index` consulta el modelo `Clase` y envía el resultado al template a través de un `context`, siguiendo el patrón vista → modelo → context.
- `gimnasio.views.tip_del_dia` consume un **microservicio propio** (ver abajo), que a su vez consulta una base de datos PostgreSQL en la nube (Supabase), distinta a la SQLite/PostgreSQL que usa este proyecto Django.

## Microservicio propio

Repositorio: https://github.com/Arthoss/forja-microservicio

Es una API construida con Flask, desplegada en Render (`https://forja-microservicio.onrender.com`), que se conecta a una base de datos PostgreSQL alojada en Supabase para devolver tips de entrenamiento aleatorios en formato JSON (`GET /api/tip`).

## Despliegues

- Render: https://forja-gimnasio.onrender.com
- PythonAnywhere: https://arthoss444.pythonanywhere.com

## Stack

Django, SQLite (local) / dj-database-url, Whitenoise, Requests, Gunicorn.