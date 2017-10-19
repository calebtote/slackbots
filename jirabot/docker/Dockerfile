FROM python:2

COPY /jira.pem /
COPY / /jirabot/
RUN pip install slackclient schedule jira PyJwt cryptography
WORKDIR /jirabot
#CMD [ "python", "jbot.py" ]
ENTRYPOINT [ "/jirabot/entrypoint.sh" ]
