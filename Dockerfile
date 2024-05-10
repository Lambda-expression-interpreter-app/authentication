FROM python:3.11
WORKDIR /app
RUN pip install requests
RUN pip install flask
COPY . /app
CMD ["python3","auth.py"]