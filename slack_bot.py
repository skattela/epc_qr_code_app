import slack


def send_file_to_slack(file_path, title="SEPA QR Code", channel="finanzen"):
    # slack_token = os.getenv("slack_token")
    slack_token = "xoxb-241729836977-953130526979-c1hXpI82EnJLIHzjAJ87Qi8y"

    client = slack.WebClient(token=slack_token)

    client.files_upload(
        channels=channel,
        file=file_path,
        title=title
    )
