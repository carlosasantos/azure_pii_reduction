from conversation_pii import sample_conv_pii_transcript_input
from pii_recognition import sample_pii_recognition
from data_prep import prep_input_data, prep_print_data
from ast import literal_eval

def default_api(document):
    results, redacted = sample_pii_recognition(document)

    redacted_formatted = redacted
    new_str2 = '<span style="background-color:red">' + '*' + '</span>'
    redacted_formatted = redacted_formatted.replace('*', new_str2)
    redacted_formatted = redacted_formatted.replace('\n', '\\\n')
    redacted_formatted = redacted_formatted.replace('\t', '&emsp;')
    # redacted_formatted = redacted_formatted.replace('*', '\\*')
    redacted_formatted_form = redacted_formatted.replace('*', '\\*')

    return redacted, redacted_formatted, redacted_formatted_form

def format_print(document):
    redacted_formatted = document
    new_str = '<span style="background-color:red">' + '[REDACTED]' + '</span>'

    redacted_formatted = redacted_formatted.replace('[REDACTED]', new_str)
    redacted_formatted = redacted_formatted.replace('\n', '\\\n')
    redacted_formatted = redacted_formatted.replace('\t', '&emsp;')

    return redacted_formatted

def conversational_api(document):

    conversation = prep_input_data(document)

    body={
        "displayName": "Analyze PII in conversation",
        "analysisInput": {
            "conversations": [
                {
                    "conversationItems": conversation,


                    "modality": "transcript",
                    "id": "1",
                    "language": "en"
                }
            ]
        },
        "tasks": [
            {
                "taskName": "redact PII",
                "kind": "ConversationalPIITask",
                "parameters": {
                    "modelVersion": "2022-05-15-preview",
                    "redactionSource": "text",
                    "piiCategories": [
                        "all"
                    ]
                }
            }
        ]
    }

    redacted = sample_conv_pii_transcript_input(body)
    # print(redacted)
    output_clean = str()
    output_formatted = str()
    for i, result in enumerate(redacted['conversations'][0]['conversationItems']):
        conversation_id = literal_eval(result['id'])
        if conversation_id == conversation[i]['id']:
            participantId = conversation[i]['participantId']
            text_clean = result['redactedContent']['text']
            text_formatted = result['redactedContent']['text']
            
            new_str2 = '<span style="background-color:red">' + '*' + '</span>'
            text_formatted = text_formatted.replace('*', new_str2)

            new_string_formatted = f"{participantId}&emsp;{text_formatted}\\\n"
            new_string_clean = f"{participantId}\t{text_clean}\n"
            # print(f'{participantId}\t{text}\n')
            output_formatted = output_formatted + new_string_formatted
            output_clean = output_clean + new_string_clean
        else:
            raise IndexError("ID's do not match")
    output_formatted = output_formatted.strip('\n').strip('\\')
    output_clean = output_clean.strip('\n')
    # redacted = prep_print_data(redacted)
    return output_clean, output_formatted, redacted


def combine_two_apis(document: str):

    redacted_default, _, _ = default_api(document)

    redacted_conv, _, _ = conversational_api(document)

    if len(redacted_default) != len(redacted_conv):
        raise ValueError(f'Length mismatch: \n\tDefault API: {len(redacted_default)} characters\n\tConversational API: {len(redacted_conv)} characters\n')
    else:
        print(f'Default API: {len(redacted_default)} characters\nConversational API: {len(redacted_conv)} characters\n')

    new_string_clean = str()
    for element in zip(redacted_default,redacted_conv):
        new_string_clean += overlap_redaction(element)

    new_str2 = '<span style="background-color:red">' + '*' + '</span>'
    new_string_formatted = new_string_clean.replace('*', new_str2)
    new_string_formatted = new_string_formatted.replace('\n', '\\\n')
    new_string_formatted = new_string_formatted.replace('\t', '&emsp;')

    
    return new_string_clean, new_string_formatted

def overlap_redaction(element: tuple):
    if (element[0] != '*') & (element[1] != '*') & (element[0] != element[1]):
        raise ValueError('Character Mismatch') 

    if element[0] == '*':
        return element[0]
    if element[1] == '*':
        return element[1]
    if element[0] == element[1]:
        return element[0]
    # <span style="color:blue">some *blue* text</span>

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

def insert_str2(string, str_to_insert, offset, length):
    return string[:offset] + str_to_insert + string[offset+length:]