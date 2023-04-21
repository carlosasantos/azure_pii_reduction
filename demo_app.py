import json
# from data_prep import prep_input_data, prep_print_data
from call_apis import default_api, format_print, conversational_api, combine_two_apis
import streamlit as st
import os

# with open('cred.json', 'r') as f:
#     cred = json.load(f)


st.set_page_config(layout="wide")


st.title('PII Redaction Demo')

option0 = st.selectbox(
    'Select Redaction API',
    ('PII Entity Recognition', 'Conversational PII', 'Combine APIs'))

option1 = st.selectbox(
    'Select Input',
    ('Existing Files', 'New Input'))


def table(redacted_clean_formatted, redacted_original_formatted):

    table_headers = """
    <tr>
    <th>Fake PII</th>
    <th>Original Cut</th>
    </tr>
    """
    html_table = """<table id='pii_table'>"""
    html_table = html_table + table_headers
    left_redacted = redacted_clean_formatted.split('\\\n')
    right_original = redacted_original_formatted.split('\\\n')
    if len(left_redacted) == len(right_original):
        for i, row in enumerate(left_redacted):
            row_left = row
            row_right = right_original[i]
            new_row = f'<tr><td>{row_left}</td><td>{row_right}</td></tr>'
            html_table = html_table + new_row
        html_table = html_table + '</table>'
        return html_table
    else: 
        raise IndexError('Data length does not match')
    


if option1 == 'Existing Files':

    file_list = os.listdir('data')
    file_list = [f.split(' - ')[0] for f in file_list]
    file_list = set(file_list)
    file_list2 = ['']
    file_list2.extend(file_list)
    option2 = st.selectbox(
        'Select Existing Case',
        file_list2)

    if option2:
        with open(f'data/{option2} - Typist_Redacted - Fake PII.json', 'r') as f:
            clean = f.read()
        with open(f'data/{option2} - Typist_Redacted - Original cut.json', 'r') as f:
            redact = f.read() 
        
        redacted_original_formatted = format_print(redact)

        if option0 == 'PII Entity Recognition':
            _ , redacted_clean_formatted, _ = default_api(clean)
        if option0 == 'Conversational PII':
            _ , redacted_clean_formatted, _ = conversational_api(clean)
        if option0 == 'Combine APIs':
            _, redacted_clean_formatted = combine_two_apis(clean)

        table_html = table(redacted_clean_formatted, redacted_original_formatted)
        st.markdown(table_html, unsafe_allow_html=True) 


if option1 == 'New Input':
    with st.form("Input"):
        queryText = st.text_area("Text to Redact (Only Default API):", height=3, max_chars=None)
        btnResult = st.form_submit_button('Submit')
    
    if btnResult:
        _, _, redacted_formatted_form = default_api(queryText)
        st.markdown(redacted_formatted_form, unsafe_allow_html=True)





# col1, col2 = st.columns(2)
# with col1:
#     with st.form("InputRedacted"):
#         queryText = st.text_area("Text to Redact:", height=3, max_chars=None)
#         btnResult1 = st.form_submit_button('Submit')

#     if btnResult1:
#         # data = prep_input_data(queryText)
#         st.markdown('hello world', unsafe_allow_html=True)
#     # output = prep_print_data(data)
#     # st.markdown(output, unsafe_allow_html=True)

# with col2:
#     with st.form("InputValidation"):
#         redactedText = st.text_area("Redacted Text (to validate):", height=3, max_chars=None)
#         btnResult2 = st.form_submit_button('Submit')

    # if btnResult2:
        # data = prep_input_data(queryText)
        # st.markdown('hello world', unsafe_allow_html=True)
# option = st.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone'))
# file_list = os.listdir('data')
# file_list = [f.split(' - ')[0] for f in file_list]
# file_list = set(file_list)
# option = st.selectbox(
#     'How would you like to be contacted?',
#     file_list)

# if option == 'Home phone':
#     with st.form("InputRedactesadsd"):
#         queryText = st.text_area("Text to Redact:", height=3, max_chars=None)
#         btnResult1 = st.form_submit_button('Submit')

# st.write('You selected:', option)



st.markdown(
    """
    <style>
        div[class="row-widget stButton"]
                {
                    # border:1px solid red;
                    text-align: end;
                    # vertical-align: bottom;
                }
        #pii_table td {
                    width:50%;
                    vertical-align: top;
                    text-align: left;
                    border: 1px solid white !important;
                    border-collapse: collapse !important; 
                    border-spacing: 0 !important; 
                    border-bottom: 1px solid white !important;
                    border-top: 1px solid white !important;
                }
        #pii_table th {
                    width:50%;
                    text-align: center;
                    # color: red; 
                    # border: 1px solid blue !important;
                    border-collapse: collapse !important;
                    border-bottom: 1pt solid black !important;
                    border-top: 1pt solid white!important;
                    border-left: 1pt solid white !important;
                    border-right: 1pt solid white !important; 
                }
        #pii_table {
                    width:100%;
                    # border: 1px solid red;
                    # border-collapse: collapse;
                }
        table[id=pii_table], th, td {
                    border: 1px solid white !important;
                    # bordercolor: red !important;
                    border-collapse: collapse !important;        
                }

    </style>
    """,unsafe_allow_html=True
)




