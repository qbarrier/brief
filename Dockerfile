FROM python:3.12-slim-bookworm

WORKDIR /app/

### installation de dépendance pour bibliothèque python ###
RUN pip install requests pandas

### COPY DU FICHIER .PY DANS WORKDIR ###
COPY hello-world.py .
COPY import_data.py .
COPY analyse_brief.py .
COPY analyse.sql .

### COMMANDES D'EXECUTION AU LANCEMENT ###
CMD ["python", "hello-world.py"]

