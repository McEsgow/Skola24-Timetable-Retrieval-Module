import requests
import json

class API:
  x_scope = ""
  def __init__(self):
    self.session = requests.Session()
    self.base_url = "https://web.skola24.se"
    self.headers = {
      "Accept": "application/json, text/javascript, */*; q=0.01",
      "Accept-Language": "en-US,en;q=0.5",
      "Content-Type": "application/json",
      "X-Scope": self.x_scope,
      "X-Requested-With": "XMLHttpRequest",
      "Origin": self.base_url,
      "Connection": "keep-alive",
    }

  # Function to get signature
  def get_signature(self, signature:str):
    """
    Retrieves an encrypted signature for the given signature string.

    Args:
      signature (str): The signature string to encrypt.

    Returns:
      str: The encrypted signature.
    """
    url = f"{self.base_url}/api/encrypt/signature"
    payload = json.dumps({"signature": signature})
    response = self.session.post(url, headers=self.headers, data=payload)
    return response.json()['data']['signature']

  # Function to get key
  def get_key(self):
    """
    Retrieves the key required to render the timetable.

    Returns:
      str: The key required to render the timetable.
    """
    url = f"{self.base_url}/api/get/timetable/render/key"
    response = self.session.post(url, headers=self.headers, data=json.dumps(None)) # data-raw null
    return response.json()['data']['key']


  def get_active_school_years(self, host_name:str, check_school_years_features:bool=False):
    """
    Returns a JSON object containing information about the active school years for the specified host.

    Args:
      host_name (str): The name of the host for which to retrieve active school years.
      check_school_years_features (bool, optional): Whether to check for school year features. Defaults to False.

    Returns:
      dict: A JSON object containing information about the active school years.
    """
    url = f"{self.base_url}/api/get/active/school/years"
    payload = {
      "hostName":host_name,
      "checkSchoolYearsFeatures":check_school_years_features
    }
    
    response = self.session.post(url, headers=self.headers, json=payload)
    return response.json()

  def get_units(self, host_name:str):
      """
      Retrieves a list of units (schools) associated with the specified host name.

      Args:
          host_name (str): The name of the host to retrieve units for.

      Returns:
          list: A list of units (schools) associated with the specified host name.

      Raises:
          ValueError: If the specified host name is not found.
          Exception: If there is an error with the API response.
      """
      url = f"{self.base_url}/api/services/skola24/get/timetable/viewer/units"
      payload = {
        "getTimetableViewerUnitsRequest": {
          "hostName": host_name
        }
      }
      response = json.loads(self.session.post(url, headers=self.headers, json=payload).text)
      if not response['data'].get('validationErrors'):
        return response['data']['getTimetableViewerUnitsResponse']['units']
      elif response['data']['validationErrors'][0]['id'] == 1:
        raise ValueError(f'Host {host_name} not found')
      else:
        raise Exception(f'Error: {response["data"]["validationErrors"]}')
    
    
  # Function to get timetable
  def get_timetable(self, render_key, host_name, unit_guid, signature, school_year_guid, week, year):
    """
    Retrieves the timetable for a given school unit, week and year.

    Args:
      render_key (str): The render key for the school unit.
      host_name (str): The host name for the school unit.
      unit_guid (str): The GUID for the school unit.
      signature (str): The selection signature for the timetable.
      school_year_guid (str): The GUID for the school year.
      week (int): The week number for the timetable.
      year (int): The year for the timetable.

    Returns:
      dict: The JSON response from the API containing the timetable data.
    """
    url = f"{self.base_url}/api/render/timetable"
    payload = {
      "renderKey": render_key,
      "host": host_name,
      "unitGuid": unit_guid,
      "selection": signature,
      "schoolYear": school_year_guid,
      #"startDate": "2023-11-06", 
      #"endDate": "2023-11-08",
      #"scheduleDay": 0, #
      #"blackAndWhite": False, #
      "width": 500,
      "height": 615,
      "selectionType": 4,
      #"showHeader": False, #
      #"periodText": "", #
      "week": week,
      "year": year,
      #"privateFreeTextMode": False, #
      #"privateSelectionMode": None, #
      #"customerKey": "", #
    }
    
    #print(json.dumps(payload, indent=2))
    
    response = self.session.post(url, headers=self.headers, data=json.dumps(payload))
    return response.json()



def get_timetable(host_name:str, unit_name, schema_id:str, week:int, year:int):
  """
  Returns a list of lessons for a given week and year, for a specific unit and schema ID.

  Args:
  - host_name (str): The name of the host.
  - unit_name (str): The name of the unit.
  - schema_id (str): The schema ID.
  - week (int): The week number.
  - year (int): The year.

  Returns:
  - A list of dictionaries, where each dictionary represents a lesson and contains the following keys:
    - title (str): The title of the lesson.
    - date (str): The date of the lesson in the format "YYYY-MM-DD".
    - start_time (str): The start time of the lesson in the format "HH:MM".
    - end_time (str): The end time of the lesson in the format "HH:MM".
    - teacher (str): The name of the teacher.
    - location (str): The location of the lesson.
  """
  api = API()
  
  # Get unit guid
  units = api.get_units(host_name)
  unit_guid = None
  for unit in units:
    if unit['unitId'] == unit_name:
      unit_guid = unit['unitGuid']
      
  if not unit_guid:
    raise ValueError(f'Unit {unit_name} not found in {host_name}')

  # Get school year guid
  school_year_guid = api.get_active_school_years(host_name)['data']['activeSchoolYears'][0]['guid']
  
  
  render_key = api.get_key()
  signature = api.get_signature(schema_id)
  
  timetable_data = api.get_timetable(render_key, host_name, unit_guid, signature, school_year_guid, week, year)
  
  if not len(timetable_data['validation']) > 0:
  
    dates = {}
    
    for item in timetable_data["data"]["textList"]:
      if item['type'] == 'HeadingDay':
        day_of_week = item['text'].split(' ')[0]
        day = item['text'].split(' ')[1].split('/')[0]
        month = item['text'].split(' ')[1].split('/')[1]
        
        dates[{'Måndag':1, 'Tisdag':2, 'Onsdag':3, 'Torsdag':4, 'Fredag':5,}[day_of_week]] = {'day':day, 'month':month}

    lessons = []
    for lesson in timetable_data["data"]["lessonInfo"]:
      teacher = lesson['texts'][1] if len(lesson['texts']) > 1 else ''
      location = lesson['texts'][2] if len(lesson['texts']) > 2 else ''
      lessons.append({
        'title': lesson['texts'][0],
        'date': f"{year}-{dates[lesson['dayOfWeekNumber']]['month']}-{dates[lesson['dayOfWeekNumber']]['day']}",
        'start_time': lesson['timeStart'],
        'end_time': lesson['timeEnd'],
        'teacher': teacher,
        'location': location,
      })
      
    return lessons

  elif timetable_data['validation'][0]['code'] == 4:
    raise ValueError(f'Schema ID not found in {host_name}/{unit_name}')
  else:
    raise f"Error: {timetable_data['validation']}"
  
  
  

# Example usage

host_name = 'lerum.skola24.se'
unit_name = 'Lerums gymnasium'
schema_id = 'te2b'
week = 45
year = 2023
API.x_scope = '8a22163c-8662-4535-9050-bc5e1923df48'

schema = get_timetable(host_name, unit_name, schema_id, week, year)
print(schema)
