# Skola24 Timetable Retrieval Module

This Python module allows for the retrieval of timetables from the Skola24 system by interacting with their API. The module offers a simple interface to access different endpoints to obtain information such as the timetable for a specific school unit, week, and year.

## Disclaimer

This software is an independent wrapper for the Skola24 API and is not affiliated with, authorized, maintained, sponsored, or endorsed by Skola24 or any of its affiliates or subsidiaries. This is an unofficial wrapper and is designed for educational purposes only.

The Author of this software does not claim ownership of any data retrieved from the Skola24 API and makes no guarantees about the quality, accuracy, or completeness of any information or data provided by this software. Users of this wrapper are responsible for complying with all terms and conditions of the Skola24 API.

By using this software, you acknowledge that you have read and agree to comply with the terms and conditions of the Skola24 API and understand that the Author is not responsible for any violations of those terms.


## Installation

The module does not need installation via package managers like pip. Instead, you can directly import it into your Python project as shown below:

```python
import skola24
```

## Configuration

Before you start retrieving timetables, you must set the `x_scope` attribute of the `API` class to your specific 'x_scope_value'.

```python
skola24.api.x_scope = "your_xscope_value"
```

## Usage

To get a timetable, you can use the `get_timetable` function with the required parameters:

```python
timetable = skola24.get_timetable(host_name, unit_name, schema_id, week, year)
```

---
Please replace `your_xscope_value`, `host_name`, `unit_name`, `schema_id`, `week`, and `year` with actual values before running the code.

## API Reference

Below are the core functionalities provided by the module.

### `API` Class

This class encapsulates the methods to interact with the Skola24 API endpoints. It handles sessions, headers, and the generation of necessary keys and signatures.

#### Methods

- `get_signature`: Returns an encrypted signature for the provided string.
- `get_key`: Retrieves the key necessary to render the timetable.
- `get_active_school_years`: Returns information about the active school years for a given host.
- `get_units`: Retrieves a list of school units associated with a host name.
- `get_timetable`: Fetches the timetable for a specific school unit, week, and year.

### `get_timetable` Function

This standalone function provides a high-level interface to retrieve a list of lessons for a given unit and schema ID within a specific week and year.

### Example

Here is an example showing how to retrieve a timetable for a specified week and year:

```python
import skola24

host_name = 'lerum.skola24.se'
unit_name = 'Lerums gymnasium'
schema_id = 'te2b'
week = 45
year = 2023
skola24.API.x_scope = 'your_xscope_value'

schema = skola24.get_timetable(host_name, unit_name, schema_id, week, year)
print(schema)
```

## Contributions

Contributions to this module are welcome. Please ensure that you provide adequate documentation for your code and that it adheres to the project's code style.

## License

### Grant of License

The Author grants users of this software a non-exclusive, revocable license to use, modify, and maintain the software solely for personal and educational purposes, and to contribute to its repository on GitHub or similar platforms designated by the Author, subject to the following restrictions:

1. **Non-Commercial Use**: Users are not permitted to use this software for commercial purposes.

2. **No Redistribution**: Users are not allowed to redistribute the software or any derivative works.

3. **Contribution**: Contributions to the software by submitting patches, improvements, or modifications are allowed, but they become the property of the software's repository and its owner(s). Contributions must also adhere to the same restrictions as stated in this license.

4. **Attribution**: Users must give appropriate credit to the original Author, provide a link to the source of the software, and indicate if changes were made when contributing or sharing the software in a non-commercial setting.

### Termination

This license is effective until terminated. The license will terminate automatically without notice from The Author if the user fails to comply with any provision contained herein. Upon termination, the user must destroy all copies of the software.

The Author reserves the right to terminate the license at any time and for any reason, at The Author's sole discretion. Upon termination, the user agrees to cease all use and destroy all copies of the software immediately. Any such termination may be effected without prior notice to the user. Continued use of the software following notice of termination constitutes an infringement of copyright, and legal action may be taken to enforce this termination.

### Disclaimer of Warranty

The software is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

### Limitation of Liability

In no event shall The Author be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

---

All other rights reserved by skola24.