FROM python:3.11
WORKDIR /app
RUN pip install requests
COPY . /app
CMD ["python3","auth.py"]