# Python 2.7 Run Time Base Image
FROM python:2.7

MAINTAINER John Yang (john.yang20@berkeley.edu)

# Setting Working Directory to "App" Folder in container
WORKDIR /app

# Copy current directory's contents into "App" Folder within container
ADD . /app

# Miscellaneous Updates
RUN apt-get update

# Install required packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available to world outside container (TODO(john-b-yang): Necesary?)
EXPOSE 8000

# Enter shell when container launches
CMD ["/bin/sh"]
