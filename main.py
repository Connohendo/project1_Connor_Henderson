import sys
import requests
import sqlite3
from secret import wufoo_key
from requests.auth import HTTPBasicAuth


# def main():

def get_wufoo_data() -> dict:  # comment to test workflow
    url = "https://chendro.wufoo.com/api/v3/forms/zk890sm1gnzlxu/entries/json"
    response = requests.get(url, auth=HTTPBasicAuth(wufoo_key, 'pass'))

    if response.status_code != 200:
        print(f"Failed to get data, response code: {response.status_code} and error message: {response.reason}")
        sys.exit(-1)

    jsonresponse = response.json()
    return jsonresponse['Entries']


def write_wufoo_data():
    # create a database connection
    conn = sqlite3.connect('wufoo_db.db')
    cursor = conn.cursor()

    # create the table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries
                 (Entry_Id text,
                  Title text,
                  First_Name text,
                  Last_Name text,
                  Org_Title text,
                  Organization text,
                  Email text,
                  Org_Website text,
                  Phone_Number text,
                  Time_Period text,
                  Permission text,
                  Opportunities text,
                  Date_Created text,
                  Created_By text,
                  Date_Updated text,
                  Updated_By text)''')

    # retrieve the data from Wufoo
    data = get_wufoo_data()

    # insert the data into the table
    for item in data:
        cursor.execute("INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (item['EntryId'],
                   # title
                   item.get('Field5', ''),
                   # first name
                   item.get('Field6', ''),
                   # last name
                   item.get('Field7', ''),
                   # org title
                   item.get('Field8', ''),
                   # org
                   item.get('Field1', ''),
                   # email
                   item.get('Field10', ''),
                   # website
                   item.get('Field9', ''),
                   # phone number
                   item.get('Field12', ''),
                   # Time period
                   ', '.join([item.get('Field213', ''),
                              item.get('Field214', ''),
                              item.get('Field215', ''),
                              item.get('Field216', ''),
                              item.get('Field217', '')]),
                   # perms
                   item.get('Field313', ''),
                   # opportunities
                   ', '.join([item.get('Field113', ''), item.get('Field114', ''), item.get('Field115', ''),
                              item.get('Field116', ''), item.get('Field117', ''), item.get('Field118', ''),
                              item.get('Field119', '')]),
                   # created
                   item.get('DateCreated', ''),
                   # created by
                   item.get('CreatedBy', ''),
                   # date updated
                   item.get('DateUpdated', ''),
                   # updated by
                   item.get('UpdatedBy', '')))
    # commit the changes to the database and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #main()
    write_wufoo_data()
