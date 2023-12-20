# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]
import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    def listDrive(drive_id):
      pageToken = None
      while True:
        results = (
          service.files()
          .list(pageToken=pageToken, pageSize=1000,corpora='drive', driveId=drive_id, includeItemsFromAllDrives=True, includeTeamDriveItems=True, supportsAllDrives=True, supportsTeamDrives=True, fields="nextPageToken, files(id, name, mimeType, driveId, size, modifiedTime, createdTime, shortcutDetails, parents)")
          .execute()
        )
        items = results.get("files", [])
        for item in items:
          yield item
        pageToken = results.get("nextPageToken", None)
        if pageToken == None:
          break
    
    def write_csv(out_file, drive_id):    
      with open(out_file, 'w') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(['Id', 'Name', 'MimeType', 'Size', 'Created Time', 'Modified Time', 'ParentId', 'Shortcut Target Id', 'Shortcut Target MimeType'])
        for item in listDrive(drive_id):
          writer.writerow([item['id'], item['name'], item['mimeType'], item.get('size', None), item['createdTime'], item['modifiedTime'], item.get('parents', [None])[0], item.get('shortcutDetails', {}).get('targetId'), item.get('shortcutDetails', {}).get('targetMimeType')])

  
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
# [END drive_quickstart]
