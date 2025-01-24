from google.cloud import translate
from google.api_core.retry import Retry
from google.api_core.exceptions import DeadlineExceeded

class Translator:
    def __init__(self, project_id: str, timeout: int = 30):
        self.project_id = project_id
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{self.project_id}"
        self.timeout = timeout
        self.retry = Retry(
            initial=1.0,  # seconds
            maximum=10.0,  # seconds
            multiplier=1.5,
            deadline=60.0  # total timeout in seconds
        )

    def translate_text(self, text: str, target_language_code: str) -> translate.Translation:
        try:
            response = self.client.translate_text(
                parent=self.parent,
                contents=[text],
                target_language_code=target_language_code,
                timeout=self.timeout,
                retry=self.retry
            )

            return response.translations[0]
        except DeadlineExceeded as e:
            print("Request timed out. Please try again later.")
            return None

if __name__ == "__main__":
    PROJECT_ID = '--redacted project ID--'
    translator = Translator(PROJECT_ID)

    text = "Hi, my name is John. I am a software engineer."
    target_language = "hi"

    print(f" {text} ".center(50, "-"))
    translation = translator.translate_text(text, target_language)
    source_language = translation.detected_language_code
    translated_text = translation.translated_text
    print(f"{source_language} → {target_language} : {translated_text}")
