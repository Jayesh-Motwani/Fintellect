from GoogleNews import GoogleNews
import requests
import json


googlenews = GoogleNews(start='06/30/2024', end='06/30/2025')
googlenews.search('pharma cipla')
results = googlenews.results()
print(results)
SCHEMA={
    "news_summary":{"type":"string"}
}
prompt = f"""
{json.dumps(SCHEMA)}
Return a summary of the given text in JSON schema given
Only provide the summary in the JSON file
{results}

"""

def call_ollama(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "news_summ",
        "prompt": prompt,
        "format": "json",
        "options": { "temperature": 0.7 }
    }, timeout=120,stream=True)
    r.raise_for_status()
    # the /generate endpoint streams; concatenate 'response' chunks
    data = ""
    for line in r.iter_lines():
        if not line: continue
        obj = json.loads(line.decode())
        data += obj.get("response","")
        if obj.get("done"): break
    return data


raw = call_ollama(prompt)
print(raw)