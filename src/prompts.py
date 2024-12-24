import time
from google.genai import Client, types
from src.config.settings import settings

SYSTEM_PROMPT = """When given a video and a query, call the relevant function only once with the appropriate timecodes 
and text for the video"""

USER_PROMPT = """For each scene in this video, generate captions that describe the scene along with any spoken text 
placed in quotation marks. Place each caption into an object sent to set_timecodes with the timecode of the caption 
in the video."""

client = Client(api_key=settings.GOOGLE_API_KEY)




class VideoAnalyzer:

    def __init__(self, client: Client = client, model: str = settings.MODEL,
                 user_prompt: str = USER_PROMPT, system_prompt:str = SYSTEM_PROMPT):

        self.client = client
        self.model = model
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        self.uploaded_file = None
        self.response = None


    def upload_file(self, video_path: str):

        self.uploaded_file = client.files.upload(path=video_path)
        while self.uploaded_file.state == "PROCESSING":
            print('Waiting for video to be processed.')
            time.sleep(10)
            self.uploaded_file = client.files.get(name=self.uploaded_file.name)

        if self.uploaded_file.state == "FAILED":
            raise ValueError(self.uploaded_file.state)
        print(f'Video processing complete: ' + self.uploaded_file.uri)


    def analyze(self):

        self.response = client.models.generate_content(
            model=self.model,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(
                            file_uri=self.uploaded_file.uri,
                            mime_type=self.uploaded_file.mime_type),
                    ]),
                USER_PROMPT,
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.0,
            ),
        )

        return self.response