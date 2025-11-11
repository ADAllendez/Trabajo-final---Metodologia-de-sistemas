#!/bin/bash

echo "======================================"
echo " 🚀 Iniciando Sistema de Turnos Médicos"
echo "======================================"

# --- BACKEND SETUP ---
echo ""
echo "📦 Verificando entorno backend..."

cd backend || exit

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
  echo "🧰 Creando entorno virtual..."
  python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias si falta algo
if [ -f "requirements.txt" ]; then
  echo "📥 Instalando dependencias backend..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "⚠️ No se encontró requirements.txt en backend/"
fi

# Iniciar backend en segundo plano
echo "🩺 Iniciando servidor FastAPI..."
uvicorn app.main:app --reload --port 8000 &
BACK_PID=$!

cd ..

# --- FRONTEND SETUP ---
echo ""
echo "💻 Verificando entorno frontend..."

cd frontend || exit

# Instalar dependencias npm si no existen
if [ ! -d "node_modules" ]; then
  echo "📥 Instalando dependencias frontend..."
  npm install
else
  echo "✅ Dependencias frontend ya instaladas."
fi

# Iniciar frontend (Vite)
echo "🌐 Iniciando servidor React..."
npm run dev &

FRONT_PID=$!

cd ..

# --- MENSAJE FINAL ---
echo ""
echo "======================================"
echo " ✅ Backend corriendo en: http://localhost:8000"
echo " ✅ Frontend corriendo en: http://localhost:5173"
echo "======================================"
echo ""
echo "Presiona CTRL+C para detener ambos servidores."

# Esperar procesos
wait $BACK_PID $FRONT_PID