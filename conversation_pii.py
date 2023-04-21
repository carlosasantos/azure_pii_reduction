# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
FILE: sample_conv_pii_transcript_input.py
DESCRIPTION:
    This sample demonstrates how to analyze a conversation for PII (personally identifiable information).
    For more info about how to setup a CLU conversation project, see the README.
USAGE:
    python sample_conv_pii_transcript_input.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_CONVERSATIONS_ENDPOINT                       - endpoint for your CLU resource.
    2) AZURE_CONVERSATIONS_KEY                            - API key for your CLU resource.
"""

def sample_conv_pii_transcript_input(payload):
    # [START analyze_conversation_app]
    # import libraries
    import os
    import json
    from azure.core.credentials import AzureKeyCredential

    from azure.ai.language.conversations import ConversationAnalysisClient

    # get secrets
    # endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
    # key = os.environ["AZURE_CONVERSATIONS_KEY"]

    # get credentials
    with open('cred.json', 'r') as f:
        cred = json.load(f)
    endpoint = cred.get('endpoint')
    key = cred.get('key')

    # analyze quey
    client = ConversationAnalysisClient(endpoint, AzureKeyCredential(key))
    with client:

        poller = client.begin_conversation_analysis(
            task=payload
        )

        # view result
        result = poller.result()
        task_result = result["tasks"]["items"][0]
        # print("... view task status ...")
        # print(f"status: {task_result['status']}")
        conv_pii_result = task_result["results"]
        if conv_pii_result["errors"]:
            print("... errors occurred ...")
            for error in conv_pii_result["errors"]:
                print(error)
        else:
            conversation_result = conv_pii_result["conversations"][0]
            if conversation_result["warnings"]:
                print("... view warnings ...")
                for warning in conversation_result["warnings"]:
                    print(warning)
    return conv_pii_result


    # [END analyze_conversation_app]


if __name__ == '__main__':
    sample_conv_pii_transcript_input()