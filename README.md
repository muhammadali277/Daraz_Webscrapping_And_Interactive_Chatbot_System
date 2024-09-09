# Advanced Mobile Product Web Scraping and Interactive Chatbot System

Project Overview
This project is an advanced mobile product analysis system that performs web scraping, intelligent chatbot development, and dashboard creation. It extracts detailed information about mobile products from Daraz.pk, processes the data, and allows users to interact with it via a chatbot. The project also features a dashboard that presents the data in an insightful and interactive way.

Key Features
Web Scraping: Extracts mobile product data (name, price, brand, reviews) from the first five pages of Daraz.pk and stores it in CSV format. Irrelevant products, such as accessories, are filtered out during the scraping process.

Chatbot Development: An intelligent chatbot is developed using Flask and a pre-trained Transformer model to handle user queries. The chatbot supports various types of queries, including price-based, brand-based, and specification-based searches.

Dashboard: A web-based dashboard is created using Flask to visualize product data. It provides insights into top products, average prices, and ratings, and includes a query interface for interacting with the chatbot.

Use Cases
1. Price-Based Queries
Command: "Show me phones under Rs. 30,000."
Action: Returns a list of mobile phones priced below Rs. 30,000.

Command: "List phones between Rs. 20,000 and Rs. 50,000."
Action: Returns a list of mobile phones priced between Rs. 20,000 and Rs. 50,000.

2. Brand-Based Queries
Command: "Show me Samsung mobiles."
Action: Lists all available Samsung mobile phones from the data.

Command: "Give me Apple brand mobile phones."
Action: Lists all Apple mobile phones in the dataset.

3. Specifications-Based Queries
Command: "Best phone with 128GB storage."
Action: Returns phones that match the specification of 128GB storage.

4. Rating-Based Queries
Command: "Show me phones with over 4.5-star rating."
Action: Lists all phones that have a rating of 4.5 stars or higher.

5. Review-Based Queries
Command: "Show me the best-reviewed phone."
Action: Returns the phone with the highest average review score.

Command: "List phones with the most reviews."
Action: Returns phones that have the highest number of reviews.

6. Product Search Queries
Command: "Search phone iPhone 13 Pro."
Action: Finds and returns details of the iPhone 13 Pro from the dataset.

Command: "Find Samsung Galaxy S21."
Action: Searches for and returns details of the Samsung Galaxy S21.

7. Combination Queries
Command: "Show me phones under Rs. 40,000 with over 4.0-star rating."
Action: Returns phones that meet both criteria (price and rating).

Command: "List Xiaomi phones under Rs. 50,000 with a rating above 4.2."
Action: Filters and returns Xiaomi phones that are priced under Rs. 50,000 and have a rating higher than 4.2 stars.

8. Exit Query
Command: "Exit"
Action: Ends the conversation, resets the conversation history, and prepares the system for a new session.
