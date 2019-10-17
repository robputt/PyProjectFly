import argparse
import csv
from pyprojectfly import Client


def main():
    parser = argparse.ArgumentParser(description='Fetch your ProjectFly logbook as a CSV.')
    parser.add_argument('email', nargs=1)
    parser.add_argument('password', nargs=1)
    parser.add_argument('outfile', nargs=1)

    args = parser.parse_args()
    email = args.email[0]
    password = args.password[0]
    outfile = args.outfile[0]

    client = Client(email, password)
    logbook_items = client.list_logbook()

    with open(outfile, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(['Callsign',
                             'Flight Number',
                             'Start Time',
                             'End Time',
                             'Status',
                             'Departure ICAO',
                             'Departure Name',
                             'Arrival ICAO',
                             'Arrival Name',
                             'Aircraft Registration',
                             'Aircraft Type',
                             'Airline',
                             'Network',
                             'Landing Rate (FPM)'])
        for logbook_item in logbook_items:
            flight = logbook_item.get('flight')

            if flight.get('time_started'):
                start_time = flight.get('time_started')
            else:
                start_time = None

            if flight.get('time_ended'):
                end_time = flight.get('time_ended')
            else:
                end_time = None

            if flight.get('landing_fpm'):
                landing_fpm = flight.get('landing_fpm')
            else:
                landing_fpm = None

            departure = logbook_item.get('departure')
            arrival = logbook_item.get('arrival')
            aircraft = logbook_item.get('aircraft')
            airline = aircraft.get('airline')

            csv_writer.writerow([logbook_item.get('callsign'),
                                 logbook_item.get('flight_number'),
                                 start_time,
                                 end_time,
                                 logbook_item.get('status'),
                                 departure.get('icao'),
                                 departure.get('name'),
                                 arrival.get('icao'),
                                 arrival.get('name'),
                                 aircraft.get('registration'),
                                 aircraft.get('type'),
                                 airline.get('name'),
                                 logbook_item.get('network'),
                                 landing_fpm])

if __name__ == '__main__':
    main()
