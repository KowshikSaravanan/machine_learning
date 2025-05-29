#!/bin/bash

echo "Starting entrypoint.sh with APP=$APP"

if [ "$APP" = "fastapi" ]; then
  echo "Launching FastAPI server..."
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
elif [ "$APP" = "streamlit" ]; then
  echo "Launching Streamlit app..."
  exec streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
else
  echo "ERROR: Specify APP=fastapi or APP=streamlit"
  exit 1
fi
