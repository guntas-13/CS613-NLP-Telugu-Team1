# ES613-NLP

## File Structure

1. Directory `<SourceName>-<TeamMemberName>` should contain `LinkScrape` directory where the Link scraping codes are present and `WebCrawl` directory where the Text Parsing from each weblink codes are present.
2. Additionally the main directory `<SourceName>-<TeamMemberName>` can contain the Jupyter Notebook where a dry run must have taken place before making the scraping and crawling links.
3. `badwords.json` contains the JSON file of Telugu + English bad words that are to be removed from the text.
4. `HuggingFace.ipynb` demonstrates how existing corpus in `.parquet` can be dowloaded.
5. Later these `.parquet` files have to be read using `pandas` and then have to be parsed for each row to get the text into separate `.txt` files.

### [Telugu Corpus Sheet](https://docs.google.com/spreadsheets/d/1Kr59i-8Gyhi3ehN_hLVCPdBcms7L07xNUUFsTW3uFDk/edit?gid=1042635267#gid=1042635267)

### SQuAD Paper

[SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) <br>
[Paper Overview](https://sh-tsang.medium.com/brief-review-squad-100-000-questions-for-machine-comprehension-of-text-f191c6b670b8) <br>
[Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) <br>
[Dependency Parsing](https://towardsdatascience.com/natural-language-processing-dependency-parsing-cf094bbbe3f7) <br>
[Universal Dependency Table](https://universaldependencies.org/u/dep/) <br>
