# Skola24 API Client

This code provides a Python API client for accessing timetable data from the Skola24 platform.


## Setup

To use this API client, you will need to retrieve your X-Scope, which you will find as a header in every request to skola 24. Use your browsers inbuilt inspection tool (`Ctrl+Shift+I` on chrome and firefox). You find requests under the `Network` tab.

Once retrieved, set it using `set_auth_token(<YOUR_X-SCOPE>)`


## Usage

The main method for retrieving timetable data is `get_timetable()`



### `get_timetable()`:


#### Parameters:

- `host_name`: The name of the school's host in the Skola24 system.
- `unit_id`: The ID of the unit for which you want to retrieve the timetable.
- `schema_id`: The ID of the schema for which you want to retrieve the timetable.
- `year`: The year for which you want to retrieve the timetable.
- `week`: The week for which you want to retrieve the timetable.
- `raw` (optional): If set to `True`, returns the raw HTTP response instead of the parsed timetable data.


#### Return:
A list of dictionaries, each representing a lesson in the timetable. The dictionaries contain the following keys:

- `title`: The title of the lesson.
- `teacher`: The name of the teacher teaching the lesson.
- `location`: The location of the lesson.
- `time_start`: The start time of the lesson, in ISO format.
- `time_end`: The end time of the lesson, in ISO format.
- `date`: The date of the lesson, in ISO format.

If there are no lessons, the function will return `"no_activities"`.





### Example
```python
import skola_24_api
skola_24_api.set_auth_token("abcd1234")

timetable = skola_24_api.get_timetable("host", "unit", "schema", 2022, 1)
```

This returns a list of lessons, each containing title, teacher, location, start/end times, and date.

```json
[
{
    "title": "Math", 
    "teacher": "Mrs. Johnson",
    "location": "Room 201",
    "time_start": "08:00",
    "time_end": "09:00", 
    "date": "2022-01-03"
},
...
]
```


## Helper Methods

There are additional helper methods for retrieving unit info, render keys, and schema signatures needed for the `get_timetable()` call:

- `get_unit_guid()`
- `get_render_key()`
- `get_schema_signature()`

### `get_render_key(host_name, unit_id)`

Retrieves the key needed to retrieve a timetable for a specific school and unit.


- `host_name`: The name of the school's host in the Skola24 system.
- `unit_id`: The ID of the unit for which you want to retrieve the timetable.

Returns the key needed to retrieve a timetable for the specified school and unit.

### `get_unit_guid(host_name, unit_id)`

Retrieves the unit GUID needed to retrieve a timetable for a specific school and unit.

- `host_name`: The name of the school's host in the Skola24 system.
- `unit_id`: The ID of the unit for which you want to retrieve the timetable.

Returns the unit GUID needed to retrieve a timetable for the specified school and unit.

### `get_schema_signature(host_name, unit_id, schema_id)`

Retrieves the signature needed to retrieve a timetable for a specific school, unit, and schema.

- `host_name`: The name of the school's host in the Skola24 system
- `unit_id`: The ID of the unit for which you want to retrieve the timetable.
- `schema_id`: The ID of the schema for which you want to retrieve the timetable.


## Error Handling

The `get_timetable()` method will raise a `ValidationError` if the API returns an error. The exception contains the error code and message from Skola24.

Here is an additional notes/acknowledgements section added to the end:

## Acknowledgements

- This API client is unofficial and not endorsed by Skola24

- The developer assumes no responsibillity for how the code is being used.

- The developer accepst no liability directly or indiriectly arising from use.

- Usage of Skola24's API should only be used in accordance with their terms of service

- Information retrieved from the API should only be used in accordance with Skola24's terms of service
