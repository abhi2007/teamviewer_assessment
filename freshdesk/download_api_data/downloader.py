import json, re

from freshdesk.download_api_data.api_request import FreshdeskApiRequest
from freshdesk.util import output_data_to_file


def download_daily_report():
    """Downloads a daily report from the Freshdesk API"""

    # Object to store the tickets information from the API
    output_data = []

    # Initiate the class
    api_client = FreshdeskApiRequest()
    # Query the API to get the report with the ticket information
    report_data = api_client.request_report()
    # Process the ticket data
    tickets = json.loads(report_data)
    tickets = json.dumps(tickets)

    # Get the output file nam
    output_file_name = api_client.get_output_file()
    output_file = output_file_name if str(output_file_name).endswith('.gz') \
        else str(output_file_name) + '.gz'

    output_data.append(tickets)
    file_date = int(re.search(r'\d+', output_file).group())

    # write the data to the file with compression
    print(f'writing the tickets information for ' + str(file_date))
    output_data_to_file(data='\n'.join(output_data), filepath=output_file, compressed=True)
