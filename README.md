# Scraper to [La Republica](https://www.larepublica.co/)

Web scraping is data scraping used for extracting data from websites. The web Scraping software may directly access the World Wide Web using the Hypertext Transfer Protocol or a web browser. 

Our script will extract information from the website of a Colombian newspaper ([La Republica](https://www.larepublica.co/)). 
It uses [XPATH](https://en.wikipedia.org/wiki/XPath) so changes to the website frontenfd will requiere changes to the Xpath.

The news are saved in .txt files inside a folder with the date. It can be run daily and will extract:
* Title
* Author
* Resume
* Body

## Requeriments
* request
* lxml
