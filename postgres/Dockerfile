# name:tag
FROM python:3.11.4

# set up working directory
WORKDIR /code

# packages to install
COPY ./requirements.txt code/requirements.txt

RUN yes | apt-get update
# clears cache and install requirements
RUN pip install --no-cache-dir --upgrade -r code/requirements.txt

# specify what to copy
COPY ./app code/app

# run commands after starting the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]