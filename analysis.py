import json
import requests


def process_pdata(pdata):
    file = open('data/input.json', 'w')
    input_json = {'question': {}, 'name': pdata['name'], 'gender': pdata['gender'], 'birthplace': pdata['birthplace'], 'birthyear': pdata['birthyear'], 'residence': pdata['residence'], 'job': pdata['job']}

    if 'message' in pdata:
        input_json['message'] = pdata['message']

    if 'pets[]' in pdata:
        input_json['pets'] = {}
        for n in range(len(pdata['pets[]'])):
            input_json['pets'][n] = pdata['pets[]'][n]

    job_value = 0

    for n in range(1, 21):
        question = 'question[' + str(n) + ']'
        job_value += int(pdata[question][0])
        input_json['question'][n] = pdata[question][0]

    json.dump(input_json, file, indent=6)

    best_job_value = 0
    if pdata['job'] == ['ceo']:
        best_job_value = 60

    elif pdata['job'] == ['astronaut']:
        best_job_value = 54

    elif pdata['job'] == ['doctor']:
        best_job_value = 50

    elif pdata['job'] == ['model']:
        best_job_value = 50

    elif pdata['job'] == ['rockstar']:
        best_job_value = 62

    elif pdata['job'] == ['garbage']:
        best_job_value = 62

    job_suitability = 5 - abs(int((best_job_value - job_value)/10))

    birthyear = str(pdata['birthyear'][0])
    movie_id = 'tt' + str(job_value % 2) + str(job_value-1) + birthyear

    uri = 'http://omdbapi.com'
    gdata = {'apikey': 'ec496fe2', 'i': movie_id, 'r': 'json'}
    response = requests.get(uri, params=gdata)

    output = response.json()

    profile_data = {'career': {'desired': pdata['job'][0], 'suitability': job_suitability}, 'movie': output}

    if 'pets[]' in pdata:
        profile_data['pets'] = {}
        for pet in pdata['pets[]']:
            if pet == 'dog':
                host = 'dog.ceo'
                path = 'api/breeds/image/random'
                uri = f'https://{host}/{path}'
                response = requests.get(uri)

                print(response.json())
                url = response.json()['message']
                pic = requests.get(url)

                filename = url.split('/')[-1]
                picture_path = 'data/' + filename
                with open(picture_path, 'wb') as fout:
                    fout.write(pic.content)

                profile_data['pets']['dog'] = filename

            if pet == 'cat':
                host = 'api.thecatapi.com'
                path = 'v1/images/search'
                uri = f'https://{host}/{path}'
                response = requests.get(uri)

                print(response.json())
                url = response.json()[0]['url']
                pic = requests.get(url)

                filename = url.split('/')[-1]
                picture_path = 'data/' + filename
                with open(picture_path, 'wb') as fout:
                    fout.write(pic.content)

                profile_data['pets']['cat'] = filename

            if pet == 'duck':
                host = 'random-d.uk'
                path = 'api/v2/random'
                uri = f'https://{host}/{path}'
                response = requests.get(uri)

                print(response.json())
                url = response.json()['url']
                pic = requests.get(url)

                filename = url.split('/')[-1]
                picture_path = 'data/' + filename
                with open(picture_path, 'wb') as fout:
                    fout.write(pic.content)

                profile_data['pets']['duck'] = filename

    profile_file = open('data/profile.json', 'w')
    json.dump(profile_data, profile_file, indent=6)
