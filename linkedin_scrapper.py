import requests
import csv

def linkedin_search(first_name, last_name):
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'client_id': '77ke0cd350gbs3',
        'client_secret': 'Ax3g7xENqFU2cVhz',
        'grant_type': 'client_credentials',
        'Content-Type': 'application/web_scrapper',
    }
    access_token = requests.post(token_url, data=data)  # The access token that has to be generated using the POST command
    #print(access_token)
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

