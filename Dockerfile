FROM python:3.10.0b3-slim

COPY . /

RUN pip install -r requirements.txt
RUN pip install connexion[swagger-ui]

#ENV webhook_api_token ${webhook_api_token}
#ENV jira_url ${jira_url}
#ENV jira_user ${jira_api_token}
#ENV jira_api_token ${jira_api_token}
#ENV slack_api_token ${slack_api_token}

CMD python main.py