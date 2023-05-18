# for all files in data/actstxt/*.txt submit to Cohere summarizer 
# and keep output into data/actstxt/summaries/*.txt

import glob
import os

import dotenv
dotenv.load_dotenv()

import cohere

co = cohere.Client(api_key=os.environ.get('COHERE_API_KEY'))

for fn in glob.glob('data/actstxt/*.txt'):
    print(fn)
    if os.path.isfile(fn.replace('actstxt', 'summaries')):
        print('Already summarized', fn)
        continue
    with open(fn, 'r') as fhand:
        text = fhand.read()

    if len(text) > 10000:
        print(f"Truncating {fn} due to size {len(text)} exceeding 10k chars")
        text = text[:10000]

    response = co.summarize( 
        text,
        model='summarize-xlarge', 
        length='long',
        extractiveness='medium',
        format='paragraph'
    )

    with open(fn.replace('actstxt', 'summaries'), 'w+') as fhand:
        fhand.write(response.summary)



