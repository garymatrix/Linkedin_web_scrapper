import requests
import csv

def linkedin_search(first_name, last_name):
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = { 
        'grant_type': 'client_credentials',
        'client_id': '77neftb6ngfgo0',
        'client_secret': 'R0im1KwnmvId164g',
        'Content-Type': 'application/x-www-form-urlencoded',
        'redirect_uri': 'https://www.linkedin.com/in/garymatrix/'
    }
    response = requests.post(token_url, data=data)  

    if response.status_code==200:
        try:
         access_token = response.json()['access_token']
        except KeyError:
         print("Acess token not found")
         print (response.json)
         return None
    else:
        print(f"Failed to retrieve acess token. Status Code: {response.status_code}")
        print("Response:", response.text)
        return None


    url = f'https://api.linkedin.com/v2/people-search?q=fullName&firstName={first_name}&lastName={last_name}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        profiles = []
        for person in data['elements']:
            profile = {
                'Name': f"{person['firstName']} {person['lastName']}",
                'Profile URL': person['publicProfileUrl'],
                'Headline': person['headline'],
                'Location': person['location']['name'],
                'Industry': person['industryName'],
            }
            profiles.append(profile)
        return profiles
    else:
        print("Error", response.status_code)

def save_csv(data):
    if data:
        csv_file = 'profiles.csv'
        fields = ['Name', 'Profile URL', 'Headline', 'Location', 'Industry' ]
        with open(csv_file, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
            print("Data saved successfully")
    else:
        print("Operation unsuccessful")

def main():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    data = linkedin_search(first_name, last_name)
    save_csv(data)
    
if __name__ == "__main__":
    main()

