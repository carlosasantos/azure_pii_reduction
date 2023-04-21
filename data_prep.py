
def prep_input_data(data):
    data_list = data.split('\n')
    conversation = []
    counter = 0
    for element in data_list:
        counter += 1
        element_split = element.split('\t')
        element_dict = {'participantId': element_split[0],
                        'id': counter,
                        'text': element_split[1],
                        'lexical': element_split[1]}
        # print(element_dict.get('participantId'))
        conversation.append(element_dict)
    return conversation

def prep_print_data(data: list):

    output = str()
    for element in data:
        new_string = f"**{element['participantId']}**&emsp;{element['text']}\\\n"
        output = output + new_string
        print(new_string)
    output = output.strip('\n').strip('\\')
    # output = output + 'a'
    return output