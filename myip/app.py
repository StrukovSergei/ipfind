from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Your IP</title>
    <style>
      body {font-family: Arial, Helvetica, sans-serif; display:flex; min-height:100vh; align-items:center; justify-content:center;}
      .box {text-align:center; color:#0a8a00;}
      .big {font-size:48px; font-weight:700;}
    </style>
  </head>
  <body>
    <div class="box">
      <h1>Your IP address is:</h1>
      <div class="big">{{ ip }}</div>
    </div>
  </body>
</html>
"""

def get_client_ip():
    # Prefer real client headers when behind proxies or CDNs
    header_order = [
        "CF-Connecting-IP",
        "True-Client-IP",
        "X-Forwarded-For",  # may contain comma separated list
        "X-Real-IP",
        "X-Client-IP",
        "Fastly-Client-Ip",
    ]
    for h in header_order:
        v = request.headers.get(h, "")
        if v:
            return v.split(",")[0].strip()
    # Fallback to the peer address
    ra = request.remote_addr or ""
    return ra.split(":")[0] if ":" in ra else ra

@app.get("/")
def index():
    return render_template_string(HTML, ip=get_client_ip())

# plain text endpoint for curl or uptime checks
@app.get("/ip.txt")
def ip_txt():
    return get_client_ip() + "\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
