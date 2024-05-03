import requests
import csv

def linkedin_search(first_name, last_name, access_token):

    #url = f'https://api.linkedin.com/v2/people-search?q=fullName&firstName={first_name}&lastName={last_name}' #previous url
    url = 'https://api.linkedin.com/v2/people' #url 
    headers = {
        'Authorization': f'Bearer {access_token}', #default as specified by the api
        'Content-Type': 'application/json' #content needs to be fetched in json
    }
    parameters = {
        'q': f'firstName:{first_name} AND lastName:{last_name}', #query parameters, passed seperately instead of specifying them in the url
        'projection': '(id,firstName,lastName,publicProfileUrl, headline, location, industryName)' 
    }
    response = requests.get(url, headers=headers, params= parameters)
    if response.status_code == 200:
        data = response.json() 
        profiles = []
        for person in data['elements']:
            profile = {
                'Name': f"{person['firstName']} {person['lastName']}", #extraction of each element seperately
                'Profile URL': person['publicProfileUrl'],
                'Headline': person['headline'],
                'Location': person['location']['name'],
                'Industry': person['industryName'],
            }
            profiles.append(profile) #saving profile elements in the list
        return profiles
    else:
        print("Error", response.status_code) 

def save_csv(data):           #function to save all of the data extracted in csv file
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
    access_token = '' #Direct acess token provided by LinkedIn's api
    data = linkedin_search(first_name, last_name, access_token)
    save_csv(data)
    
if __name__ == "__main__":
    main()
