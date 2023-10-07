# Ask Ellen White
A generative AI search engine based on the full text of Steps to Christ.

## How Does the App Work?
The front-end of the app (the text, prompt bar, etc.) is built in Python using Streamlit. I used a Python-based web scraper equipped with Beautiful Soup to load a Xata serverless database with the following schema for each paragraph of Steps to Christ: book name, paragraph content, paragraph reference, & chapter url. I then used Xata's ask functionality to build the generative AI component. When a prompt is submitted, Xata completes a full-text search of the database (filtered to search paragraph content only), identifies the highest-scoring paragraphs, and sends them to OpenAI via the Xata API as context for the prompt. OpenAI's response includes the database ID's for each paragraph referenced. I display the generated response and use some Python combined with Streamlit's magic to display the referenced paragraphs, along with links to the full quote context.

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
1. Update *ref* schema (and web scraper) to only include the page number.
2. Add full text of all Ellen White's writings in public domain. This will involve updating the web scraper to omit forwards, prefaces (etc.) and books/periodicals published after 1928.
3. Xata starts charging for AI calls after 250/month. If I begin exceeding that, I'm planning to build a Llama 2 model on a Runpod serverless GPU to serve as a replacement API for generative text.

## License

[MIT](https://choosealicense.com/licenses/mit/)