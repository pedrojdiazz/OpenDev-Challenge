# OpenDev Challenge

## Descripción

Este proyecto es una aplicación web que combina un frontend estático y un backend desarrollado con FastAPI. El frontend está construido en una imagen Docker y servido a través de Nginx, mientras que el backend utiliza FastAPI con SQLAlchemy y PostgreSQL para la persistencia de datos. La aplicación permite gestionar y visualizar información sobre los leads requeridos.

## Requisitos

- Docker: Asegúrate de tener Docker instalado en tu máquina.

## Instrucciones

1. **Clona el repositorio**

git clone git@github.com:pedrojdiazz/OpenDev-Challenge.git
2. **Navega al directorio del proyecto**

cd OpenDev-Challenge
3. **Crea un archivo .env**
Crea un archivo llamado `.env` en la raíz del proyecto con las siguientes variables:

makefile
DATABASE_HOSTNAME=db
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=
DATABASE_NAME=

4. **Construye la imagen Docker**

docker-compose build

5. **Levanta los contenedores**

docker-compose up

Esto iniciará tanto el frontend estático como el backend en sus respectivos contenedores Docker.

6. **Correr los tests**
Para ejecutar las pruebas, usa el siguiente comando:

docker-compose -f docker-compose.test.yml run --rm tests

## Componentes de la Aplicación

### Estructura de Carpetas

- **models/**: Contiene los modelos de base de datos para Course y Lead.
- `Lead`: Registra datos de estudiantes junto con la fecha de registro. Utiliza relationship de SQLAlchemy para asociarse con Course.
- `Course`: Almacena información sobre cursos, como la materia, el número de veces que el lead cursó la materia y el año de inscripción.

**Nota**: La estructura actual está diseñada de manera sencilla para ajustarse a los requerimientos inmediatos del proyecto. Para futuras escalabilidades, se podrían considerar optimizaciones como separar en tablas más específicas con responsabilidades más claras.

- **routes/**: Contiene el router de la aplicación con los endpoints disponibles.
- **schemas/**: Incluye las interfaces Pydantic para los modelos de Course y Lead, tanto para entrada como salida de datos.
- **services/**: Encapsula la lógica de la aplicación. Incluye métodos para interactuar con los modelos y la base de datos, y realiza validaciones.
- **test/**: Contiene las pruebas para los servicios. Las pruebas se centran en la lógica de los servicios.
- **database/**: Configuración e instanciación de la base de datos, con manejo adecuado de sesiones.

### Endpoints

- Frontend Estático: `http://localhost:80`
- API Leads: `http://localhost:8000/api/leads`
- Documentación de API: `http://localhost:8000/docs`

## Funcionalidades Adicionales

- **Paginación**: Utiliza el método `paginate` de FastAPI con SQLAlchemy para gestionar la paginación en las consultas.

## Consideraciones

- Se ha configurado un logger para registrar errores en la consola y se han implementado manejos de excepciones específicos. Aún se pueden mejorar estas características según sea necesario.
- La aplicación está modularizada y sigue buenas prácticas y patrones de diseño para mantener la calidad del código y facilitar el mantenimiento.
