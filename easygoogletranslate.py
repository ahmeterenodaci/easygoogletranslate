import concurrent.futures
import requests
import re
import os
import html
import urllib.parse

class EasyGoogleTranslate:

    '''
        Unofficial Google Translate API. 

        This library does not need an api key or something else to use, it's free and simple.
        You can either use a string or a file to translate but the text must be equal to or less than 5000 character. 
        You can split your text into 5000 characters to translate more.

        Google Translate supports 108 different languages. You can use any of them as source and target language in this application.
        If source language is not specified, it will detect source language automatically.
        This application supports multi thread translation, you can use it to translate multiple languages at once.
        Detailed language list can be found here:  https://cloud.google.com/translate/docs/languages


        Examples:
            #1: Specify default source and target language at beginning and use it any time.
                translator = GoogleTranslateRequest(
                    source_language='en',
                    target_language='de',
                    timeout=10
                )
                result = translator.translate('This is an example.')
                print(result)

            #2: Don't specify default parameters.
                translator = GoogleTranslateRequest()
                result = translator.translate('This is an example.', target_language='tr')
                print(result)

            #2: Override default parameters.
                translator = GoogleTranslateRequest(target_language='tr')
                result = translator.translate('This is an example.', target_language='fr')
                print(result)

            #4: Translate a text in multiple languages at once via multi-threading.
                translator = GoogleTranslateRequest()
                result = translator.translate(text='This is an example.', target_language=['tr', 'fr', 'de'])
                print(result)

            #5: Translate a file in multiple languages at once via multi-threading.
                translator = GoogleTranslateRequest()
                result = translator.translate_file(file_path='text.txt', target_language=['tr', 'fr', 'de'])
                print(result)

    '''

    def __init__(self, source_language='auto', target_language='tr', timeout=5):
        self.source_language = source_language
        self.target_language = target_language
        self.timeout = timeout
        self.pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'

    def make_request(self, target_language, source_language, text, timeout):
        escaped_text = urllib.parse.quote(text.encode('utf8'))
        url = 'https://translate.google.com/m?tl=%s&sl=%s&q=%s'%(target_language, source_language, escaped_text)
        response = requests.get(url, timeout=timeout)
        result = response.text.encode('utf8').decode('utf8')
        result = re.findall(self.pattern, result)
        if not result:
            print('\nError: Unknown error.')
            f = open('error.txt')
            f.write(response.text)
            f.close()
            exit(0)
        return html.unescape(result[0])

    def translate(self, text, target_language='', source_language='', timeout=''):
        if not target_language:
            target_language = self.target_language
        if not source_language:
            source_language = self.source_language
        if not timeout:
            timeout = self.timeout
        if len(text) > 5000:
            print('\nError: It can only detect 5000 characters at once. (%d characters found.)'%(len(text)))
            exit(0)    
        if type(target_language) is list:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.make_request, target, source_language, text, timeout) for target in target_language]
                return_value = [f.result() for f in futures]
                return return_value
        return self.make_request(target_language, source_language, text, timeout)

    def translate_file(self, file_path, target_language='', source_language='', timeout=''):
        if not os.path.isfile(file_path):
            print('\nError: The file or path is incorrect.')
            exit(0)
        f = open(file_path)
        text = self.translate(f.read(), target_language, source_language, timeout)
        f.close()
        return text