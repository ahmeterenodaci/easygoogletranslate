# easygoogletranslate
        
Unofficial Google Translate API. 

This library does not need an api key or something else to use, it's free and simple.
You can either use a string or a file to translate but the text must be equal to or less than 5000 character. 
You can split your text into 5000 characters to translate more.

Google Translate supports 108 different languages. You can use any of them as source and target language in this application.
If source language is not specified, it will detect source language automatically.
This application supports multi thread translation, you can use it to translate multiple languages at once.
Detailed language list can be found here:  https://cloud.google.com/translate/docs/languages

## Installation:
The easiest way to install easygoogletranslateis to download it from PyPI. Then you will be able to use the library.

```
pip install easygoogletranslate
```


## Examples:
1. Specify default source and target language at beginning and use it any time.
```
from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate(
    source_language='en',
    target_language='de',
    timeout=10
)
result = translator.translate('This is an example.')

print(result) 
# Output: Dies ist ein Beispiel.
```

2. Don't specify default parameters.
```
from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate()
result = translator.translate('This is an example.', target_language='tr')

print(result)
# Output: Bu bir örnektir.
```

3. Override default parameters.
```
from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate(target_language='tr')
result = translator.translate('This is an example.', target_language='fr')

print(result)
# Output: Ceci est un exemple.
```

4. Translate a text in multiple languages at once via multi-threading.
```
from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate()
result = translator.translate(text='This is an example.', target_language=['tr', 'fr', 'de'])

print(result)
# Output: ['Bu bir örnektir.', 'Ceci est un exemple.', 'Dies ist ein Beispiel.']
```

5. Translate a file in multiple languages at once via multi-threading.
```
from easygoogletranslate import EasyGoogleTranslate

translator = EasyGoogleTranslate()
result = translator.translate_file(file_path='text.txt', target_language=['tr', 'fr', 'de'])

print(result)
# Output: ['Nasılsın?', 'Comment ca va?', 'Wie geht es Ihnen?']
# Text inside file: How are you?
```
