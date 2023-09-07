import os
import requests
import json

api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

# Set the environment variable
os.environ['API_KEY'] = 'J_9tiq3gpcDlWlAMNzRpdw'

# Access the environment variable
api_key = os.environ['API_KEY']

header_dic = {'Authorization': 'Bearer ' + api_key}

urls = [
    'https://www.linkedin.com/in/cyan-ouedraogo1212/',
    'https://www.linkedin.com/in/samuel-laws-455528163/',
    'https://www.linkedin.com/in/michael-brown-37ab79159/',
    'https://www.linkedin.com/in/juanpabloweber/',
    'https://www.linkedin.com/in/rebecca-uddin-8549291a2/'
]

all_responses = []  # List to store all the responses

for url in urls:
    params = {
        'url': url,
        'fallback_to_cache': 'on-error',
        'use_cache': 'if-present',
        'skills': 'include',
        'inferred_salary': 'include',
        'personal_email': 'include',
        'personal_contact_number': 'include',
        'twitter_profile_id': 'include',
        'facebook_profile_id': 'include',
        'github_profile_id': 'include',
        'extra': 'include',
    }

    response = requests.get(api_endpoint, params=params, headers=header_dic)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        all_responses.append(response_data)
        print(f"Response for {url} added to the list")
    else:
        print(f"Request for {url} failed with status code:", response.status_code)

# Save all the responses to a JSON file
filename = "all_responses.json"
with open(filename, 'w') as file:
    json.dump(all_responses, file)
    print(f"All responses saved to {filename}")


#----------------------------------------------------------------------------------------------------------------------------------------------------


# import os
# import requests
# import json
# import yaml

# api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

# # Set the environment variable
# os.environ['API_KEY'] = 'J_9tiq3gpcDlWlAMNzRpdw'

# # Access the environment variable
# api_key = os.environ['API_KEY']

# header_dic = {'Authorization': 'Bearer ' + api_key}

# urls = [
#     'https://www.linkedin.com/in/cyan-ouedraogo1212/',
#     'https://www.linkedin.com/in/samuel-laws-455528163/',
#     'https://www.linkedin.com/in/michael-brown-37ab79159/',
#     'https://www.linkedin.com/in/juanpabloweber/',
#     'https://www.linkedin.com/in/rebecca-uddin-8549291a2/'
# ]

# all_responses = []  # List to store all the responses

# for url in urls:
#     params = {
#         'url': url,
#         'fallback_to_cache': 'on-error',
#         'use_cache': 'if-present',
#         'skills': 'include',
#         'inferred_salary': 'include',
#         'personal_email': 'include',
#         'personal_contact_number': 'include',
#         'twitter_profile_id': 'include',
#         'facebook_profile_id': 'include',
#         'github_profile_id': 'include',
#         'extra': 'include',
#     }

#     response = requests.get(api_endpoint, params=params, headers=header_dic)

#     # Check if the request was successful
#     if response.status_code == 200:
#         response_data = response.json()
#         all_responses.append(response_data)
#         print(f"Response for {url} added to the list")
#     else:
#         print(f"Request for {url} failed with status code:", response.status_code)

# # Save all the responses to a YAML file
# filename = "all_responses.yaml"
# with open(filename, 'w') as file:
#     yaml.dump(all_responses, file)
#     print(f"All responses saved to {filename}")






###############################--------------------------------------------------------------------#########################################



# ['https://www.linkedin.com/in/cyan-ouedraogo1212/','https://www.linkedin.com/in/samuel-laws-455528163/',
#  'https://www.linkedin.com/in/michael-brown-37ab79159/','https://www.linkedin.com/in/juanpabloweber/']


# api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
# # api_key = os.environ['GtspUnasqTkgKGmYQey0Zw']
# # Set the environment variable
# os.environ['API_KEY'] = 'GtspUnasqTkgKGmYQey0Zw'

# # Access the environment variable
# api_key = os.environ['API_KEY']

# header_dic = {'Authorization': 'Bearer ' + api_key}
# params = {
#     'url': 'https://www.linkedin.com/in/nour-ben-gaied-727803146/',
#     'fallback_to_cache': 'on-error',
#     'use_cache': 'if-present',
#     'skills': 'include',
#     'inferred_salary': 'include',
#     'personal_email': 'include',
#     'personal_contact_number': 'include',
#     'twitter_profile_id': 'include',
#     'facebook_profile_id': 'include',
#     'github_profile_id': 'include',
#     'extra': 'include',}
# response = requests.get(api_endpoint, params=params, headers=header_dic)
# print(response.json())

# # Check if the request was successful
# if response.status_code == 200:
#     # Save response to a JSON file
#     with open('response.json', 'w') as file:
#         json.dump(response.json(), file)
#         print("Response saved to response.json")
# else:
#     print("Request failed with status code:", response.status_code)
