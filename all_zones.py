import argparse
import json
import requests
import sys
from tabulate import tabulate


class Timezone:
    def __init__(self):
        pass

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="World Time Zone Provider.")
        parser.add_argument("--match", help="list timezone information from timezone value")
        parser.add_argument(
            "--offset", type=float, help="list timezone information from timezone offset"
        )
        return parser.parse_args()

    def grab_timezone_information(self):
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json"
            )
            timezone_content = json.loads(response.text)
            return timezone_content
        except requests.exceptions.ConnectionError as e:
            print(
                "Connection does not established to URL.Check Connectivity. Error: %(error)s"
                % {"error": e}
            )
            sys.exit("Exiting Program.")

    def show_all_timezone_detail(self):
        timezone_content = self.grab_timezone_information()
        table_data = [
            [index + 1, tz["value"], tz["abbr"], tz["offset"], tz["isdst"], tz["text"]]
            for index, tz in enumerate(timezone_content)
        ]
        print(
            tabulate(
                table_data,
                headers=["SR NO", "VALUE", "ABBR", "OFFSET", "ISDST", "TEXT"],
                tablefmt="grid",
            )
        )

    def matching_value_timezone_detail(self, tz_value_input):
        timezone_content = self.grab_timezone_information()
        matching_timezones = [tz for tz in timezone_content if tz["value"] == tz_value_input]

        if matching_timezones:
            table_data = [
                [index + 1, tz["value"], tz["abbr"], tz["offset"], tz["isdst"], tz["text"]]
                for index, tz in enumerate(matching_timezones)
            ]
            print(
                tabulate(
                    table_data,
                    headers=["SR NO", "VALUE", "ABBR", "OFFSET", "ISDST", "TEXT"],
                    tablefmt="grid",
                )
            )
        else:
            print(
                "Value does not exist. See information of all timezones to verify. Retry post confirmation."
            )

    def matching_offset_timezone_detail(self, offset_input):
        timezone_content = self.grab_timezone_information()

        matching_timezones = [tz for tz in timezone_content if abs(tz["offset"]) == offset_input]

        if matching_timezones:
            table_data = [
                [index + 1, tz["value"], tz["abbr"], tz["offset"], tz["isdst"], tz["text"]]
                for index, tz in enumerate(matching_timezones)
            ]
            print(
                tabulate(
                    table_data,
                    headers=["SR NO", "VALUE", "ABBR", "OFFSET", "ISDST", "TEXT"],
                    tablefmt="grid",
                )
            )

        else:
            print(
                "Offset does not exist. See information of all timezones to verify. Retry post confirmation."
            )


def main():
    obj_timezone = Timezone()
    args = obj_timezone.parse_arguments()

    if args.match:
        obj_timezone.matching_value_timezone_detail(args.match)
    elif args.offset:
        obj_timezone.matching_offset_timezone_detail(args.offset)
    else:
        obj_timezone.show_all_timezone_detail()


if __name__ == "__main__":
    main()
