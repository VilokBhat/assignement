import requests
from bs4 import BeautifulSoup

def get_filmography(actor):
    # Format the actor name for the URL
    formatted_actor = actor.replace(" ", "+")
    
    # Send a GET request to the IMDb page of the actor's filmography
    url = f"https://www.imdb.com/find?q={formatted_actor}&s=nm"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the link to the actor's filmography page
        link = soup.find("td", class_="result_text").find("a")["href"]
        
        # Send a GET request to the actor's filmography page
        url = f"https://www.imdb.com{link}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            films = []
            
            # Find all the film titles and years from the filmography table
            for row in soup.find_all("div", class_="filmo-row"):
                title_element = row.find("b").find("a")
                year_element = row.find("span", class_="year_column")
                
                if title_element and year_element:
                    title = title_element.text.strip()
                    year = year_element.text.strip()
                    
                    films.append((title, year))
            
            # Sort the films by year in descending order
            sorted_films = sorted(films, key=lambda x: int(x[1]), reverse=True)
            
            return sorted_films
        
    return None

# Example usage
actor_name = input("Enter the name: ")
filmography = get_filmography(actor_name)

if filmography:
    print(f"Films done by {actor_name} in descending order:")
    
    for film in filmography:
        print(f"{film[0]} ({film[1]})")
else:
    print(f"No filmography found for {actor_name}.")