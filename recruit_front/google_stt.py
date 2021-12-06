# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech-to-Text sample application using gRPC for async
batch processing.
"""

import sys
import os
import re
from google.cloud import speech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/hyunn/Downloads/gcp_key.json"

# [START speech_transcribe_async]
def transcribe_file(speech_file):

    client = speech.SpeechClient()

    # [START speech_python_migration_async_request]
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",
    )

    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config=config, audio=audio)
    # [END speech_python_migration_async_request]

    #print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(result.alternatives[0].transcript)
        #print("Confidence: {}".format(result.alternatives[0].confidence))
    # [END speech_python_migration_async_response]

# [END speech_transcribe_async]

# def test_transcribe(capsys):
#     transcribe_file(os.path.join(RESOURCES, "audio.raw"))
#     out, err = capsys.readouterr()

#     assert re.search(r"how old is the Brooklyn Bridge", out, re.DOTALL | re.I)

# RESOURCES = os.path.join(os.path.dirname(__file__), "resources")

wavfile = sys.argv[1]
transcribe_file(wavfile)