import requests

response = requests.get('https://discovery.meethue.com/')

locationOfInternalipaddress = response.text.find('internalipaddress')

#print('\"internalipaddress\"의 위치 :',locationOfInternalipaddress)
#print('\"internalipaddress\" 출력 시도 :',response.text[locationOfInternalipaddress:locationOfInternalipaddress+17])

#print('internalipaddress 내용 출력 시도 :',response.text[locationOfInternalipaddress+20:-4])

ip = response.text[locationOfInternalipaddress+20:-4]

print(response.text)
print('ip 주소 :',ip)

print('HTTP 상태 코드 :',response.status_code)
