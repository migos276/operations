import requests


url=f"http://127.0.0.1:8000/restaurants/new/"

data2={
    "username": "FPKA Foods",
    "email": "fpkaorgs@gmail.com",
    "tel": 658308288,
    "quartier": "logbessus"
}


response= requests.post(url,json=data2)
print("satus: ", response.status_code)
print("réponse:",response.json())