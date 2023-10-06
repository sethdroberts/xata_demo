# xata_demo
Simple Streamlit app to demo Xata search, vector search, and OpenAI functions


Next steps is to create a vector store table for the entire dataset. Very cheap/simple using OpenAI for small documents.
Would cost approx. $3k to train all 100,000 pages of thr EGW database. So need to use Llama2 or equivalent to do it cheaply.
Once vector store is set up in Xata, should be able to do vector search and then AI calls easily.
Once that's set up, I can use the ask endpoint to set up AI-generated responses based on results.
Then I just need to replicate this app and use a web scraper to build an app using STC or similar book.
Once that's working fine, I can scrape the entire EGW repo and load it into Xata, then it's all scaled up.
Then it's just a matter of adding color and functionality and speed to the Streamlit app.

Alternatively, I could use this approach: https://xata.io/blog/keyword-vs-semantic-search-chatgpt
I could route the request through the ask endpoint twice to avoid having to create embeddings at all.
hat also means that when I switch to a serverless Runpod running Llama 2, it won't significantly increase
costs, because both queries will take place consecutively, slightly increasing server use.
This also eliminates the need to set up embeddings, cause I can do it all natively in Xata.

For this setup, here's the steps I'm taking next:
<ol>
  <li>Build a new database in Xata with desired metadata</li>
  <li>Test sending data from app to Xata</li>
  <li>Build a scraper to scrape STC into the database</li>
  <li>Build and test the DB search functions with this setup</li>
  <li>Build the "ask" functionality to query OpenAI effectively</li>
  <li>Once working successfully, deploy into production</li>
  <li>Build a web scraper to scrape entire EGW repo into a new DB</li>
  <li>Duplicate this app and use the new DB for all search queries</li>
</ol>