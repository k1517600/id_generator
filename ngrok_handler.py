from pyngrok import ngrok

ngrok.set_auth_token("2EpNTMpDiDEVAC8Z3JbvEaZqhnt_4MpesxegCzZY3YaGLBVMS")

tunnel = ngrok.connect(5000)
print(tunnel)

try:
    ngrok.get_ngrok_process().proc.wait()
except KeyboardInterrupt:
    print("zzzz")
    ngrok.kill()
