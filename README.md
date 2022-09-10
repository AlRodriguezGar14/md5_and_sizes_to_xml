# Why and what is this project

This is my first project on python and I created it as a tool to help me in my job, being more productive and less exposed to committing human errors. This is a simple script that takes the information of some files such as size and its hash and updates an XML with that information (sadly I can't upload the XML example).

For privacy I removed the URL from the code and I won't upload as public the XML I have to work on, but if you are interested in the logic, the learning path I followed and you want to see how it works, I can show an example to you.

## How it works

- Using a terminal command I get the size and the hash of each file.
- I take the information from the stdout and print it into a temporal .txt file.
- I 'clean' the content of the file so that I get the lines I need. Then I clean those lines and save the values in variables and lists.
- I search for the lines I have to edit in the XML (where I'm going to add the size and hash).
- I write the information in the XML.

## What did I learn
- First of all: The user doesn't think of the ideal scenario. There is no ideal scenario, so I had to add some try/except lines and think in the code in a way that it doesn't crash if a file is missing or I don't get the information I want.
- I learned how the subprocess work.
- I learned how to create loops.
- I learned how to scrape a XML document and debug lots of errors due to the special formatting (there is an invisible URL that if you don't have in mind breaks everything when writing on the XML)
- I learned how to use Element Tree (now that I am working on more projects I think that Beautiful Soup could be a more powerful and easy-to-use tool for working on this XML. I will try to re-write this script in the future)

## What did I achieve?
I was able to fix the problem I had and made the script work the way I wanted.
This saves me time and I avoid errors when copy-pasting the information from the terminal to the XML.
