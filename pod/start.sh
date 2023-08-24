cd /app
mkdir -p logs
. .venv/bin/activate && \
  uvicorn \
  --log-level warning \
  --no-access-log \
  --no-use-colors \
  --host 0.0.0.0 --port 3000 \
  --reload \
  fineai_task_face_recog:app &>> logs/log &