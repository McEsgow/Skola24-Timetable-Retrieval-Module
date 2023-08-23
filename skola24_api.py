import json
import requests
import urllib.parse

class ValidationError(Exception):
    pass

x_scope_ = None

def set_auth_token(x_scope):
    global x_scope_
    x_scope_ = x_scope

def verify_xscope():
    if x_scope_ == None:
        raise NameError('X-Scope not specified. Use set_auth_token(x_scope="YOUR X-SCOPE"). See documentation for retrieval instructions.')

def get_unit_guid(host_name, unit_id):
    verify_xscope()
    headers = {
        'Content-Type' : 'application/json',
        'DNT': '1',
        'Origin': 'https://web.skola24.se',
        'Referer': 'https://web.skola24.se/timetable/timetable-viewer/' + host_name + '/' + urllib.parse.quote_plus(unit_id),
        'X-Scope': x_scope_,
    }

    json_data = {'getTimetableViewerUnitsRequest': {'hostName': host_name}}
    response = requests.post('https://web.skola24.se/api/services/skola24/get/timetable/viewer/units', headers=headers, json=json_data,)
    if response.status_code == 200:
        f = open('response', 'w')
        f.write(response.text)
        f.close()
        for unit in json.loads(response.text)['data']['getTimetableViewerUnitsResponse']['units']:
            if unit['unitId'] == unit_id:
                return unit['unitGuid']
    else:
        raise Exception(response.status_code)

def get_render_key(host_name, unit_id):
    verify_xscope()

    headers = {
        'DNT': '1',
        'Origin': 'https://web.skola24.se',
        'Referer': 'https://web.skola24.se/timetable/timetable-viewer/' + host_name + '/' + urllib.parse.quote_plus(unit_id),
        'X-Scope': x_scope_,
    }

    response = requests.post('https://web.skola24.se/api/get/timetable/render/key', headers=headers)
    if response.status_code == 200:
        key = json.loads(response.text)['data']['key']
        return(key)
    else:
        raise Exception(response.status_code)
    

def get_schema_signature(host_name, unit_id, schema_id):
    verify_xscope()
    headers = {
        'Content-Type' : 'application/json',
        'DNT': '1',
        'Origin': 'https://web.skola24.se',
        'Referer': 'https://web.skola24.se/timetable/timetable-viewer/' + host_name + '/' + urllib.parse.quote_plus(unit_id),
        'X-Scope': x_scope_,
    }

    json_data = {'signature': schema_id}
    response = requests.post('https://web.skola24.se/api/encrypt/signature', headers=headers, json=json_data)
    if response.status_code == 200:
        signature = json.loads(response.text)['data']['signature']
        return(signature)
    else:
        raise Exception(response.status_code)

def get_timetable(host_name:str, unit_id:str, schema_id:str, year:int, week:int, raw=False):
    verify_xscope()
    
    headers = {
        'Content-Type' : 'application/json',
        'DNT': '1',
        'Origin': 'https://web.skola24.se',
        'Referer': 'https://web.skola24.se/timetable/timetable-viewer/' + host_name + '/' + urllib.parse.quote_plus(unit_id),
        'X-Scope': x_scope_,
    }

    json_data = {
        'renderKey': get_render_key(host_name, unit_id),
        'host': host_name,
        'unitGuid': get_unit_info(host_name, unit_id),
        'startDate': None,
        'endDate': None,
        'scheduleDay': 0,
        'blackAndWhite': False,
        'width': 512,
        'height': 512,
        'selectionType': 4,
        'selection': get_schema_signature(host_name, unit_id, schema_id),
        'showHeader': False,
        'periodText': '',
        'week': week,
        'year': year,
        'privateFreeTextMode': False,
        'privateSelectionMode': None,
    }
    response = requests.post('https://web.skola24.se/api/render/timetable', headers=headers, json=json_data)

    if raw == True:
        return response
    
    else:
        response = json.loads(response.text)
        f = open('timetable.json', 'w')
        f.write(json.dumps(response))
        f.close()
        
        #Calculate dates for the weekday-number
        
        if len(response["validation"]) == 0:
            dates = {}
            for item in response["data"]["textList"]:
                if item['type'] == 'HeadingDay':
                    dates[{'Måndag':1, 'Tisdag':2, 'Onsdag':3, 'Torsdag':4, 'Fredag':5,}[item['text'].split(' ')[0]]] = {'day':item['text'].split(' ')[1].split('/')[0], 'month':item['text'].split(' ')[1].split('/')[1]}
            
            #Interpurate lesson info
            lessons = []
            if response['data']['lessonInfo'] != None:
                for lesson in response["data"]["lessonInfo"]:
                    try: 
                        teacher = lesson['texts'][1]
                        try:
                            location = lesson['texts'][2]
                        except IndexError:
                            location = ''
                    except IndexError:
                        teacher = ''
                        try:
                            location = lesson['texts'][1]
                        except IndexError:
                            location = ''
                    
                    lessons.append({'title':lesson['texts'][0],
                                    'teacher':teacher,
                                    'location': location,
                                    'time_start':lesson['timeStart'],
                                    'time_end':lesson['timeEnd'],
                                    'date':str(year) + '-' + str(dates[lesson['dayOfWeekNumber']]['month']) + '-'  + str(dates[lesson['dayOfWeekNumber']]['day'])})
                return lessons      
            else:
                return "no_activities"
        else:
            raise ValidationError(f'{response["validation"][0]["code"]}: {response["validation"][0]["message"]}')
