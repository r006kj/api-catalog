FROM python:3-slim
WORKDIR /programas/catalogo-juegos
RUN pip3 install flask mysql-connector-python
COPY . .
EXPOSE 8001
CMD sh -c "python3 db.py && python3 app.py"
