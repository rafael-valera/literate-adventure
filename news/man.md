# Het Nieuwsblad news events
## 

### NAME

- *het nieuwsblad (hetnieuwsblad.py)*

### DESCRIPTION

- *Scraps Het Nieuwsblad website for news events (headlines)*
    
### EXAMPLE

```python
from hetnieuwsblad import HetNieuwsblad

def main():
    headlines = HetNieuwsblad.get_headlines(HetNieuwsblad.MAIN_PAGE_NEWS)
    for news_event in headlines:
        print(headline)
        print(headline.get_headline())
        print(headline.get_date())

    news_event = HetNieuwsblad.get_news_content(HetNieuwsblad.NEWS_CONTENT_EXAMPLE)
    print(news_event.get_content())


if __name__ == "__main__":
    main()
```
