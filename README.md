🏥 Sistema de Turnos Médicos

Aplicación web para la gestión integral de turnos en una clínica médica.
Permite registrar, editar, cancelar y finalizar turnos, así como gestionar pacientes, médicos y especialidades.
Desarrollada con FastAPI (backend) y React (frontend).

🧩 Tecnologías utilizadas
Backend:

Python 3.10+

FastAPI

SQLAlchemy

SQLite (base de datos local)

Uvicorn (servidor ASGI)

Pydantic

CORS Middleware

Frontend:

React + Vite

TailwindCSS

Axios

Lucide React (iconos)

ShadCN/UI (componentes estilizados)

🚀 Funcionalidades principales

✅ Crear, editar y eliminar turnos

✅ Cambiar el estado del turno (Programado, Atendiendo, Finalizado, Cancelado)

✅ Filtrar y listar pacientes, médicos y especialidades

✅ Vista tipo “Dashboard” con estado visual de cada turno

✅ Backend rápido y ligero con FastAPI

✅ Frontend moderno y responsive con React y TailwindCSS

⚙️ Estructura del proyecto
/ (raíz del repositorio)
├── backend/        # Proyecto FastAPI (Python)
│   ├── app/
│   ├── venv/
│   └── requirements.txt
│
├── frontend/       # Proyecto React (Vite)
│   ├── src/
│   ├── package.json
│   └── node_modules/
│
├── run.sh          # Script para instalar y ejecutar todo automáticamente
└── README.md

▶️ Ejecución de la aplicación

Gracias al script run.sh, no es necesario instalar manualmente dependencias ni iniciar servidores por separado.
El script se encarga automáticamente de:

Pasos para ejecutar el script run.sh

Abrí una terminal en la raíz del proyecto
(donde están las carpetas /backend, /frontend y el archivo run.sh).

Dale permisos de ejecución al archivo (solo la primera vez):

chmod +x run.sh


Ejecutá el script:

./run.sh

-- Crear el entorno virtual de Python si no existe

-- Instalar las dependencias del backend desde requirements.txt

-- Instalar las dependencias del frontend con npm install

-- Ejecutar FastAPI en http://localhost:8000

-- Ejecutar React/Vite en http://localhost:5173

Solo tenés que:

-- Tener instalado Python 3.10+, Node.js, y npm

-- Dar permisos de ejecución al script run.sh

-- Ejecutarlo desde la raíz del proyecto

Una vez iniciado, podrás acceder al frontend desde tu navegador y trabajar con el sistema de turnos completo.

📂 Dependencias principales
🔧 Backend (backend/requirements.txt)

fastapi

uvicorn

sqlalchemy

pydantic

python-multipart

💻 Frontend (frontend/package.json)

react

react-dom

vite

axios

tailwindcss

lucide-react

@radix-ui/react

@shadcn/ui

🗄️ Base de datos

La aplicación utiliza SQLite, que se genera automáticamente al ejecutar el backend.
No requiere configuración adicional.

Podés borrar el archivo database.db en la carpeta backend/ si querés reiniciar los datos.

🙌 Autores

Desarrollado por Alejo Diaz Allendez y Fabricio Nicolas Ponce
Proyecto técnico de gestión de turnos médicos — versión completa con backend y frontend integrados.
