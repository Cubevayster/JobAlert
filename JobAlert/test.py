# import the required library
from seleniumbase import Driver

# create a Driver instance with undetected_chromedriver (uc) and headless mode
driver = Driver(uc=True, headless=True)

url = 'https://fr.indeed.com/jobs?q='+"computer vision"+'&l=Lyon+%2869%29&filter=0&sort=date&from=searchOnDesktopSerp&start'

# navigate to the specified URL
driver.get(url)

# pause execution for 20 seconds
driver.sleep(20)

# take a screenshot of the current page and save it
driver.save_screenshot("datacamp.png")

# close the browser and end the session
driver.quit()