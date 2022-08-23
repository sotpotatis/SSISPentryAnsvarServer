#Docker and non-Docker setups have different file paths. Detect what is being used and start the server that should be started.
if [ "$IS_DOCKER" -eq "1" ];then
  echo "Using Docker path for starting server..."
  cd /SSISPentryAnsvarServer || exit 1
else
  echo "Using non-Docker path for starting server..."
  cd /srv/SSISPentryAnsvarServer || exit 1
fi
uvicorn main:app --host 0.0.0.0 --port 80
