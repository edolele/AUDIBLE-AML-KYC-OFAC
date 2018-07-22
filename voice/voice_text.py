import os
import wave

import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from textblob import TextBlob

textName = "KYC.txt"

text = open ( textName ).read ( )

textLower = text.lower ( )

os.system ( 'say "{}"'.format ( textLower ) )

wav = gTTS ( text=textLower , lang='en' )

wav.save ( "KYC.wav" )

translator = Translator ( )

print ( translator.translate ( text , dest='zh-CN' ).text )

'''
“了解您的客户”表格是投资行业的标准表格，可确保投资顾问了解客户的风险承受能力，投资知识和财务状况的详细信息。 KYC表格保护客户和投资顾问。
'''

text = TextBlob ( text )

print ( text.detect_language ( ) )

print ( text.sentiment )

print ( text.translate ( to='ja' ) )

'''
en
Sentiment(polarity=0.13333333333333333, subjectivity=0.25)
「あなたのクライアントを知る」フォームは、投資顧問会社が顧客のリスク許容度、投資知識および財政状態に関する詳細な情報を確実に把握する、投資業界の標準的なフォームです。 KYCフォームは、クライアントと投資顧問の両方を保護します。
'''

# Convert to WAV of FLAC with format check, then load and recognize for compatibility assurance

try:

    wav = wave.open ( "KYC.wav" , 'r' )
	
except wave.Error as e:
    
	pass

r = sr.Recognizer ( )

with sr.AudioFile ( wav ) as source:
    
	audio = r.record ( source )

print ( r.recognize_google ( audio ) )
