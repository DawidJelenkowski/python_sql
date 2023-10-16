# name:tag
FROM python:3.10

# set up working directory
WORKDIR /code

# packages to install
COPY ./requirements.txt ./

RUN yes | apt-get update
# clears cache and install requirements
RUN pip install --no-cache-dir -r requirements.txt

# specify what to copy
#COPY ./src ./src

# run commands after starting the container
CMD ["python", "--host", "0.0.0.0", "--port", "80", "--reload"]