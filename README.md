# text_mutator

This script just mutates text from a file using BERT. It's using FitBert and BertForMaskedLM for that. Note that it's definitely not sense preserving, so the result will most likely be a very different text.
The script iterates through each sentence independently and then randomly picks a word which is masked. One of the BERT models then predicts this word and the result is then taken again for the next iteration etc.

## Example
I simply took the first sentences from this NYT article: https://www.nytimes.com/2020/02/01/business/victorias-secret-razek-harassment.html?action=click&module=Top%20Stories&pgtype=Homepage

>Victoria’s Secret defined femininity for millions of women. Its catalog and fashion shows were popular touchstones. For models, landing a spot as an “Angel” all but guaranteed international stardom.

> But inside the company, two powerful men presided over an entrenched culture of misogyny, bullying and harassment, according to interviews with more than 30 current and former executives, employees, contractors and models, as well as court filings and other documents.


`python mutate_text.py test_sent.txt`
> the cradle of mankind for thousands of years. both series of the show were broadcast live. and then getting a job as an accountant all but ruined her life. while in the hospital a young woman died in an unsuccessful attempt to save women the story led to interviews with more than 100 current and former patients including doctors and nurses as well as the independent and the guardian.
