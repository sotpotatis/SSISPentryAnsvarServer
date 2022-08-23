# syntax=docker/dockerfile:1
FROM python:3.9-alpine
#Create working directory and install things
WORKDIR /SSISPentryAnsvarServer
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#Copy rest of directory
EXPOSE 80
COPY . .
#Set environmental variables
ENV IS_DOCKER=1
#Run main app
CMD "./scripts/start_pentryansvar_server.sh"
CMD "./scripts/start_pentryansvar_data_cronjob.sh"