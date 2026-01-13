#!/bin/bash

echo "======================================"
echo " 🚀 Iniciando Sistema de Turnos Médicos"
echo "======================================"

# --- BACKEND SETUP ---
echo ""
echo "📦 Configurando entorno backend..."

cd backend || exit

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
  echo "🧰 Creando entorno virtual..."
  python -m venv venv
fi

# Activar entorno virtual según sistema operativo
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  source venv/Scripts/activate
else
  source venv/bin/activate
fi

# Crear requirements.txt si no existe
if [ ! -f "requirements.txt" ]; then
  echo "📝 Creando archivo requirements.txt..."
  cat > requirements.txt <<EOL
fastapi
uvicorn
sqlalchemy
pydantic
python-multipart
aiofiles
reportlab
openpyxl
EOL
fi

# Instalar dependencias
echo "📥 Instalando dependencias del backend..."
pip install --upgrade pip
pip install -r requirements.txt

# Iniciar backend en segundo plano
echo "🩺 Iniciando servidor FastAPI..."
uvicorn app.main:app --reload &
BACK_PID=$!

cd ..

# --- FRONTEND SETUP ---
echo ""
echo "💻 Configurando entorno frontend..."

cd frontend || exit

# Instalar dependencias npm si no existen
if [ ! -d "node_modules" ]; then
  echo "📦 Instalando dependencias frontend..."
  npm install
else
  echo "✅ Dependencias frontend ya instaladas."
fi

# Verificar que existe script "start"
if ! grep -q "\"start\":" package.json; then
  echo "⚠️  No se encontró script 'start' en package.json"
  echo "🛠️  Agregalo dentro de 'scripts': { \"start\": \"react-scripts start\" }"
  exit 1
fi

# Iniciar frontend (React)
echo "🌐 Iniciando servidor React..."
npm start &
FRONT_PID=$!

cd ..

# --- MENSAJE FINAL ---
echo ""
echo "======================================"
echo " ✅ Backend corriendo en: http://localhost:8000"
echo " ✅ Frontend corriendo en: http://localhost:3000"
echo "======================================"
echo ""
echo "Presiona CTRL+C para detener ambos servidores."

# Esperar procesos
wait $BACK_PID $FRONT_PID
