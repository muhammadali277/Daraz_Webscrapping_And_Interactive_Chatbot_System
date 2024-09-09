import pandas as pd
from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Read the CSV file into a DataFrame
df = pd.read_csv('daraz_store_cleaned.csv')

# Initialize the question-answering pipeline
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Define a function to filter products based on user queries
def filter_products(query):
    if "under Rs." in query:
        max_price_str = query.split("under Rs.")[1].replace(',', '').strip()
        if '.' in max_price_str:
            max_price = float(max_price_str)
        else:
            max_price = int(max_price_str)
        filtered_df = df[df['Price'] < max_price]
        return filtered_df[['Link', 'Title', 'Price', 'Brand']]
    
    elif "brand mobile" in query:
        brand = query.split("give me")[1].replace('brand mobile', '').strip().title()
        filtered_df = df[df['Brand'] == brand]
        return filtered_df[['Link', 'Title', 'Price', 'Brand']]
    
    elif "best phone with" in query:
        specs = query.split("best phone with")[1].strip()
        filtered_df = df[df['Specifications'].str.contains(specs, case=False, na=False)]
        return filtered_df[['Link', 'Title', 'Price', 'Brand', 'Specifications']]
    
    elif "search phone" in query:
        phone_name = query.split("search phone")[1].strip().title()
        filtered_df = df[df['Title'].str.contains(phone_name, case=False, na=False)]
        return filtered_df[['Link', 'Title', 'Price', 'Brand', 'Specifications']]
    
    elif "between Rs." in query:
        price_range = query.split("between Rs.")[1].replace(',', '').strip().split(' and ')
        min_price, max_price = float(price_range[0].replace('Rs.', '').replace(',', '')), float(price_range[1].replace('Rs.', '').replace(',', ''))

        filtered_df = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
        return filtered_df[['Link', 'Title', 'Price', 'Brand', 'Specifications']]
    
    elif "show me" in query and "phones with" in query and "star rating" in query:
        min_rating = float('4.0') 
        try:
            min_rating = float(query.split("star rating")[0].split("with")[1].strip())
        except ValueError:
            pass

        filtered_df = df[df['Rating'] >= min_rating]
        return filtered_df[['Link', 'Title', 'Price', 'Brand', 'Rating']]
    
    elif "top 5 phones of" in query:
        brand = query.split("of")[1].strip().title()
        filtered_df = df[df['Brand'] == brand]
        return filtered_df.nlargest(5, 'Rating')[['Link', 'Title', 'Price', 'Brand', 'Rating']]
    
    elif "combinations should be handled" in query:
        conditions = query.split("such as")[1].strip()
        conditions_list = conditions.split("and")

        filtered_df = df
        for condition in conditions_list:
            if "price of" in condition:
                max_price_str = condition.split("price of")[1].replace(',', '').strip()
                if '.' in max_price_str:
                    max_price = float(max_price_str)
                else:
                    max_price = int(max_price_str)
                filtered_df = filtered_df[filtered_df['Price'] < max_price]
            elif "over a rating of" in condition:
                min_rating = float(condition.split("over a rating of")[1].strip())
                filtered_df = filtered_df[filtered_df['Rating'] > min_rating]
            elif "paired with a specific brand" in condition:
                brand = condition.split("paired with a specific brand like")[1].strip().title()
                filtered_df = filtered_df[filtered_df['Brand'] == brand]

        return filtered_df[['Link', 'Title', 'Price', 'Brand', 'Rating']]
    else:
        return "I'm sorry, but I couldn't understand your query."

# Function to retrieve relevant context from the data for the QA model
def get_relevant_text(df, query):
    return " ".join(df['Title'].values)  # Simplified context from all product titles

# Function to answer questions using the QA model
def answer_question(qa_model, df, query):
    context = get_relevant_text(df, query)
    result = qa_model(question=query, context=context)
    return result['answer']

# Start a conversation with the chatbot
conversation_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global conversation_history
    global df

    if request.method == 'POST':
        user_input = request.form['user_input']
        conversation_history.append("You: " + user_input)

        if user_input.lower() == 'exit':
            conversation_history = []  # Reset conversation history
            df = pd.read_csv('daraz_store_cleaned.csv')  # Reset DataFrame
            return render_template('index.html', exit_message="Goodbye!", products=None)

        # Use filter_products for structured queries
        if any(keyword in user_input for keyword in ["search phone", "under Rs.", "between Rs.", "brand mobile", "best phone with", "show me", "top 5 phones of", "combinations should be handled"]):
            products = filter_products(user_input)
            response = f"Here are the results for your query: {user_input}"
        else:
            # Use question-answering model for general queries
            response = answer_question(qa_model, df, user_input)
            products = None

        total_listings = len(df)
        avg_price = df['Price'].mean()
        avg_review_count = df['Reviews'].apply(lambda x: len(eval(x)) if pd.notna(x) else 0).mean()

        return render_template('index.html', user_input=user_input, response=response, products=products,
                               total_listings=total_listings, avg_price=avg_price, avg_review_count=avg_review_count)

    return render_template('index.html', user_input='', response='', products=None, exit_message=None)

if __name__ == '__main__':
    app.run(debug=True)
