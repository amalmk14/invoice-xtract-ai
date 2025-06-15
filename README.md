# Invoice Xtract AI

A smart tool that extracts key invoice details from PDFs or images using GPT-4 Vision, then sends the data to an API in JSON format.


## Features

- Accepts invoice files (PDF or image)
- Extracts:
  - Vendor name, invoice number, date
  - Line items (description, quantity, price)
  - Subtotal, tax, total amount
- Powered by GPT-4 Vision
- Sends extracted data to an API
- Outputs clean JSON


##  Setup

1. **Clone the repo**
    git clone https://github.com/amalmk14/invoice-xtract-ai.git
    cd invoice-xtract-ai/app

2. **Create and activate a virtual environment**
    python -m venv venv
    venv\Scripts\activate  # On Windows

3. **Install dependencies**
    pip install -r requirements.txt

4. **Add your OpenAI API key to a .env file**
    OPENAI_API_KEY=your_openai_key_here


## Usage

Put your invoice file inside the invoice_agent folder.

bash
    python main.py sample_invoice.pdf

If you don't pass a filename, it will default to:

bash
    python main.py  # uses sample_invoice.pdf



## API Output

The extracted data is sent to: https://jsonplaceholder.typicode.com/posts
You’ll see both the extracted JSON and the response from the API.
