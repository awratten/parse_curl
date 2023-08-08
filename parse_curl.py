from urllib.parse import unquote
import requests

def parse_curl(curl_string):
    headers = {}
    data = {}

    lines = curl_string.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith('curl '):
            url = (line.replace('curl "', '')[:-3])
        elif line.startswith('-H "'):
            parts = (line[4:-3].split(":"))
            header_key = parts[0]
            header_value = parts[1]
            headers[header_key] = header_value.strip()

        elif line.startswith("--data-raw"):
            data_raw = line.replace('--data-raw "', '')[:-3]
            data_items = data_raw.split("&")
            for item in data_items:
                key, value = item.split("=")
                data[key] = unquote(value.replace('^', ''))

    return url, headers, data

curl_string = """
curl "https://www.google.com" ^
  -H "authority: www.google.com" ^
  -H "accept: */*" ^
  -H "accept-language: en,en-AU;q=0.9,hu;q=0.8" ^
  -H "content-type: application/x-www-form-urlencoded; charset=UTF-8" ^
  -H "cookie: None" ^
  -H "origin: https://www.google.com" ^
  -H "referer: https://www.google.com" ^
  -H "sec-ch-ua: ^\^"Not/A)Brand^\^";v=^\^"99^\^", ^\^"Google Chrome^\^";v=^\^"115^\^", ^\^"Chromium^\^";v=^\^"115^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  -H "sec-fetch-dest: empty" ^
  -H "sec-fetch-mode: cors" ^
  -H "sec-fetch-site: same-origin" ^
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36" ^
  -H "x-requested-with: XMLHttpRequest" ^
  --compressed
"""

url, headers, data = parse_curl(curl_string)

if data == {}:
    r = requests.get(url, headers=headers)
else:
    r = requests.post(url, headers=headers, data=data)

print(r)



