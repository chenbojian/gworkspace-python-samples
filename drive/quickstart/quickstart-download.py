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
import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

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

  def download_file(file_id):
    try:
      # create drive api client
      service = build("drive", "v3", credentials=creds)

      # pylint: disable=maybe-no-member
      request = service.files().get_media(fileId=file_id, supportsTeamDrives=True, supportsAllDrives=True)
      with open(file_id, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
          status, done = downloader.next_chunk()
          print(f"{file_id} - Download {int(status.progress() * 100)}.")

    except HttpError as error:
      print(f"{file_id} - An error occurred: {error}")
      file = None

  def export_file(file_id, mimeType):
    try:
      # create drive api client
      service = build("drive", "v3", credentials=creds)

      # pylint: disable=maybe-no-member
      request = service.files().export_media(
          fileId=file_id,
          mimeType=mimeType
      )
      with open(file_id, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
          status, done = downloader.next_chunk()
          print(f"{file_id} - Download {int(status.progress() * 100)}.")

    except HttpError as error:
      print(f"{file_id} - An error occurred: {error}")
      file = None

  def upload_file(file_id, file_name, mimeType, folder_id):

    try:
      # create drive api client
      service = build("drive", "v3", credentials=creds)

      file_metadata = {"name": file_name, "parents": [folder_id]}
      media = MediaFileUpload(
          file_id, mimetype=mimeType, resumable=True
      )
      # pylint: disable=maybe-no-member
      file = (
          service.files()
          .create(body=file_metadata, media_body=media, fields="id", supportsAllDrives=True, supportsTeamDrives=True)
          .execute()
      )
      print(f'Upload File ID: "{file.get("id")}" ----> "{file_id}".')

    except HttpError as error:
      print(f"{file_id} - An error occurred: {error}")
      return None
    

  DOCX_MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  PPTX_MIME = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
  XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  PDF_MIME = 'application/pdf'
    

if __name__ == "__main__":
  main()
# [END drive_quickstart]
