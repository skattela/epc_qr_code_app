import json
import os

import requests
from requests.auth import HTTPBasicAuth

jira_url = os.getenv("jira_url")
jira_user = os.getenv("jira_user")
jira_api_token = os.getenv("jira_api_token")
auth = HTTPBasicAuth(jira_user, jira_api_token)


def get_issue_from_jira(jira_ticket):
    url = "%s/issue/%s" % (jira_url, jira_ticket)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    response_json = json.loads(response.text)
    fields = response_json.get("fields")
    name = fields.get("customfield_10046")
    iban = fields.get("customfield_10044")
    amount = fields.get("customfield_10045")
    reference = fields.get("summary")
    # print(fields.get("description").get("content")[0].get("content"))

    epc_json = {"name": name, "iban": iban, "amount": amount, "reference": reference}
    print(epc_json)
    return epc_json


def attach_to_jira(jira_ticket, file):
    print("Uploading qr_code to %s" % jira_ticket)
    url = "%s/issue/%s/attachments" % (jira_url, jira_ticket)

    headers = {
        "Accept": "application/json",
        "X-Atlassian-Token": "nocheck"
    }

    files = {'file': file}

    response = requests.request(
        "POST",
        url,
        headers=headers,
        auth=auth,
        files=files
    )
    print("Upload request send with response status %s" % response)
