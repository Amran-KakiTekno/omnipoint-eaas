with open('src/index.js', 'r', encoding='utf-8') as f:
    code = f.read()

s = code.find('<!DOCTYPE html>')
e = code.find('</html>')
html = code[s : e + len('</html>')]

p_start = code.find('const ENDPOINT_PROMPTS = {')
p_end = code.find('export default {')
prompts_raw = code[p_start : p_end].strip()

html = html.replace('const ENDPOINTS = ${endpointsJson};', prompts_raw + '\n    const ENDPOINTS = ENDPOINT_PROMPTS;')
html = html.replace("fetch('/api/execute'", "fetch('https://smart-eaas.muhammadamran40.workers.dev/api/execute'")

with open('public/index.html', 'w', encoding='utf-8') as out:
    out.write(html)

print("public/index.html written successfully. Size:", len(html))
