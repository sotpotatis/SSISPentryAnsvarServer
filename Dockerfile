# syntax=docker/dockerfile:1
FROM python:3.9-alpine
#Create working directory and install things
WORKDIR /SSISPentryAnsvarServer
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#Copy rest of directory
EXPOSE 8080
COPY . .
RUN mkdir logging
#Set environmental variables
ENV IS_DOCKER=1
ENV PENTRYANSVAR_SERVER_HOST="0.0.0.0"
ENV PENTRYANSVAR_SERVER_PORT="8080"
#Ensure permissions
#CMD "chmod +x ./scripts/start_pentryansvar_server.sh"
#CMD "chmod +x ./scripts/start_pentryansvar_data_cronjob.sh"
#Run main app
#CMD "./scripts/start_pentryansvar_server.sh"
CMD uvicorn "main:app" --host="127.0.0.1" --port="8080"
#CMD ["python", "docker_tasks.py"]
#Run redis scheduler
#CMD "rqscheduler"
#CMD "./scripts/start_pentryansvar_data_cronjob.sh"
CMD crontab crontab
CMD ["crond", "-f"]