# Ask Ellen White
A generative AI search engine based on the full text of Steps to Christ.

## How Does the App Work?
The front-end of the app (the text, prompt bar, etc.) is built in Python using Streamlit. I used a Python-based web scraper equipped with Beautiful Soup to load a Xata serverless database with the following schema for each paragraph of Steps to Christ: book name, paragraph content, paragraph reference, & chapter url. I then used Xata's ask functionality to build the generative AI component. When a prompt is submitted, Xata completes a full-text search of the database (filtered to search paragraph content only), identifies the highest-scoring paragraphs, and sends them to OpenAI via the Xata API as context for the prompt. OpenAI's response includes the database ID's for each paragraph referenced. I display the generated response and use some Python combined with Streamlit's magic to display the referenced paragraphs, along with links to the full quote context.

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
  <li>Build and test the DB search functions with STC added to DB</li>
  <li>Build the "ask" functionality to query OpenAI effectively</li>
  <li>Once working successfully, deploy into production</li>
  <li>Build a web scraper to scrape entire EGW repo into a new DB</li>
  <li>Duplicate this app and use the new DB for all search queries</li>
</ol>

Note: When creating web scraper, make sure to omit forewards, prefaces, etc.
Also, make sure to only scrape books published prior to 1915, clearly in public domain.
Also note the above + explain this is not authorized or official.
Also get the page #, not the full reference. Much more useful.

## Installation

(Assumes you have a pre-existing [Xata](https://xata.io/) database set up with the correct schema and full text of *Steps to Christ*. If not, use the scraper.py file to load it. Xata's docs are extremely helpful.)

Clone this repository: https://github.com/sethdroberts/xata_demo

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies in your local environment/Codebase.

```bash
pip install streamlit xata
```

Add the following secrets to *both* Github and Streamlit:
1. Xata API Key
2. Xata Database URL

Deploy the streamlit app in your local environment:

```bash
streamlit run app.py
```

If everything's working, deploy it to Streamlit!

## Support
Email me! Email in bio.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## Roadmap
Adding full text of all Ellen White's writings in public domain.

Xata starts charging for AI calls after 250/month. If I begin exceeding that, I'm planning to build a Llama 2 model on a Runpod serverless GPU to serve as a replacement API for generative text.

## License

[MIT](https://choosealicense.com/licenses/mit/)