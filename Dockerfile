FROM python:3.7

RUN pip install slackclient

COPY yeastizzy/__main__.py /bin/yeastizzy
RUN chmod a+x /bin/yeastizzy

LABEL "my.docker.cmd"="docker run --restart=unless-stopped --name yeastizzy --detach --network=host --env SLACK_API_KEY=$SLACK_API_KEY --env YOUTUBE_API_KEY=$YOUTUBE_API_KEY localhost:5000/yeastizzy:latest -u UC2eYFnH61tmytImy1mTYvhA"

ENTRYPOINT ["/bin/yeastizzy"]
