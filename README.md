# text_mutator

This script just mutates text from a file using BERT. It's using FitBert and BertForMaskedLM for that. Note that it's definitely not sense preserving, so the result will most likely be a very different text.
The script iterates through each sentence independently and then randomly picks a word which is masked. One of the BERT models then predicts this word and the result is then taken again for the next iteration etc.

## Examples
I simply took the first sentences from this NYT article: https://www.nytimes.com/2020/02/01/business/victorias-secret-razek-harassment.html?action=click&module=Top%20Stories&pgtype=Homepage

>Victoria’s Secret defined femininity for millions of women. Its catalog and fashion shows were popular touchstones. For models, landing a spot as an “Angel” all but guaranteed international stardom.

> But inside the company, two powerful men presided over an entrenched culture of misogyny, bullying and harassment, according to interviews with more than 30 current and former executives, employees, contractors and models, as well as court filings and other documents.


`python mutate_text.py example_nyt.txt`
> the cradle of mankind for thousands of years. both series of the show were broadcast live. and then getting a job as an accountant all but ruined her life. while in the hospital a young woman died in an unsuccessful attempt to save women the story led to interviews with more than 100 current and former patients including doctors and nurses as well as the independent and the guardian.

Another example from a CNN article: https://edition.cnn.com/2020/02/02/politics/taylor-swift-miss-americana-identity-politics/
>Taylor Swift sings about youth mobilization, endorses Democrats on Instagram and makes music videos with LGBTQ icons. She's complex, she's cool, she's an alpha type.
>The megastar hasn't always made such explicit statements, though. Lana Wilson's new documentary, "Taylor Swift: Miss Americana," charts Swift's journey from a "careful daughter" to a more self-aware pop feminist with a lot to say -- about politics and beyond.
>Indeed, the movie may be short -- 85 minutes -- but it covers meaningful territory: Swift's vulnerability ("My entire moral code, as a kid and now, is a need to be thought of as good," she admits); her eventual defiance of the same conservative mores that banished her idols, the Dixie Chicks, from the country music scene in 2003; her gradual steps toward reckoning with the at times polarizing position she occupies in, well, Americana.

`python mutate_text.py example_taylor.txt`
>he also spoke about the nature of protests on campus and the violence associated with the protests. not intimidating but more like an alpha male. the band has not released an official album yet. as a woman in america : an autobiography details her transformation from a "careful daughter" to a politically active young woman with a desire to learn about american history and culture. but the video is very short -- three minutes -- and it shows a young girl living and working in london as a place that she was a part of and thought of as good," 2 ) her deep love for the city that so strongly connected her to the beach boys and the underground music scene in london and her lack of regard for the outside world the way it was in her youth.
