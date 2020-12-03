from __future__ import print_function
import pickle
import os.path
from tqdm import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
  # Per-file access to files created or opened by the app. File authorization is granted on a per-user basis and is revoked when the user deauthorizes the app.
  'https://www.googleapis.com/auth/drive.file',
]

def main():
    # Authenticate with Google and get a Drive service client
    creds = authenticate()
    drive = build('drive', 'v3', credentials=creds)
    
    # Specify the file to upload
    directory = "/Users/nlarew/Dropbox/"
    filename = "Education booth video local.mp4"
    filepath = directory + filename
    media = MediaFileUpload(
      filepath,
      # mimetype='application/x-netcdf4',
      # mimetype='image/jpeg',
      mimetype='video/mp4',
      chunksize=1024*1024,
      resumable=True,
    )
    request = drive.files().create(
      body={'name': filename},
      media_body=media,
      fields='id',
    )
    
    # Start streaming chunks to Drive
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
          print(f"Uploaded {round(status.progress() * 100, 2)}%", end="\r")
    print("Uploaded 100%")
    print("Upload Complete!")

def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

if __name__ == '__main__':
    main()
