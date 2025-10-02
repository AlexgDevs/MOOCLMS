from pyngrok import ngrok

public_url = ngrok.connect(8000)
print(f'{public_url}')