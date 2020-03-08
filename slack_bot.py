import os

import slack


def send_file_to_slack(file_path, title="SEPA QR Code", slack_channel="dev"):
    slack_api_token = os.getenv("slack_api_token")

    client = slack.WebClient(token=slack_api_token)

    client.files_upload(
        channels=slack_channel,
        file=file_path,
        title=title
    )
