# AutoComplete proejct

### How to run the project:

1. Install the requierments.txt 
2. run the "app.py" file
You now have a server running on localhost:5000

The data.json file is pre populated with a few suggestions. 
To receive an auto complete suggestion please use the following url:
http://localhost:5000?q=<a letter you want a suggestion for, e.g. "a">

The queried data is persisted in the query.txt file. If you wish to delete a letter please use:
http://localhost:5000?delete=true
The last character specififed will be deleted as you could see in query.txt

If you wish to start a new search, either send get requests with the delete param as many times as you have characters in query.txt file, or just delete all data from the file.

In order to add additional options please send a POST request to the following api:
http://localhost:5000/add-options 
The request should entail JSON data of the form:
{
"aaa": 4,
"paq:" 12
}

