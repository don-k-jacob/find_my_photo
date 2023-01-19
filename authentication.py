from google.oauth2.credentials import Credentials
import googleapiclient.discovery

def authenticate():
    creds = Credentials.from_authorized_user_info(info=secrets)
    service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
    return service