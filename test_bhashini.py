import sys
import io

if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from bhashini_client import bhashini_client

print(f"Is Bhashini Configured: {bhashini_client.is_configured}")

test_text = "Bureau of Indian Standards ensures product quality and consumer safety."

languages = [
    ("Hindi", "hi"),
    ("Tamil", "ta"),
    ("Bengali", "bn"),
    ("Marathi", "mr")
]

for name, code in languages:
    trans = bhashini_client.translate(test_text, "en", code)
    print(f"\n[{name} ({code})]:\n  {trans}")

# Test TTS
print("\nTesting TTS (Hindi)...")
audio = bhashini_client.text_to_speech("मानक साथी में आपका स्वागत है।", "hi")
if audio:
    print(f"TTS Success! Generated {len(audio)} bytes of audio data.")
else:
    print("TTS returned no audio.")
