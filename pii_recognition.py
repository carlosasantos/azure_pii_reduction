
def sample_pii_recognition(document: str):
    from azure.core.credentials import AzureKeyCredential
    import json
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        RecognizePiiEntitiesAction
    )

    # get credentials
    with open('cred.json', 'r') as f:
        cred = json.load(f)
    endpoint = cred.get('endpoint')
    key = cred.get('key')

    credential = AzureKeyCredential(key)
    
    text_analytics_client = TextAnalyticsClient(endpoint, credential)

    documents = [document]

    poller = text_analytics_client.begin_analyze_actions(
        documents,
        display_name="Sample Text Analysis",
        actions=[
            RecognizePiiEntitiesAction()
        ]
    )

    # returns multiple actions results in the same order as the inputted actions
    document_results = poller.result()
    for doc, action_results in zip(documents, document_results):
        # print(f"\nDocument text: {doc}")
        for result in action_results:
            if result.kind == "PiiEntityRecognition":
                # print(result)
                return result, result['redacted_text']
            # print(result['redacted_text'])
            # if result.kind == "EntityRecognition":
            #     print("...Results of Recognize Entities Action:")
            #     for entity in result.entities:
            #         print(f"......Entity: {entity.text}")
            #         print(f".........Category: {entity.category}")
            #         print(f".........Confidence Score: {entity.confidence_score}")
            #         print(f".........Offset: {entity.offset}")

            # elif result.kind == "SentimentAnalysis":
            #     print("...Results of Analyze Sentiment action:")
            #     print(f"......Overall sentiment: {result.sentiment}")
            #     print(f"......Scores: positive={result.confidence_scores.positive}; "
            #         f"neutral={result.confidence_scores.neutral}; "
            #         f"negative={result.confidence_scores.negative}\n")

            # elif result.is_error is True:
            #     print(f"......Is an error with code '{result.code}' "
            #         f"and message '{result.message}'")

        # print("------------------------------------------")
    
if __name__ == "__main__":
    sample_pii_recognition(document="Microsoft was founded by Bill Gates and Paul Allen.")