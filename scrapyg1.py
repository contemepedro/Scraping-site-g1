import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_link(link):
    return link.find('a').get('href')

def get_title(title):
    return title.text

def get_class(categoria, cs):
    classes_list = [categoria]
    if(cs):
        for texto in cs:
            classes_list.append(texto.text)
    return classes_list

def get_conteudo(content):
    texto = ""
    if(content):
        for paragrafo in content:
            texto += paragrafo.text
    return texto


url = "https://g1.globo.com/economia/agronegocios/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

df = pd.DataFrame({'Título':[''], 'Classes':[''], 'Link':[''], 'Conteúdo':['']})
count_news = 0
categoria = soup.find(class_='header-editoria--link')
categoria = categoria.text

while(count_news<500):

    # encontrar as notícias da página
    for news in soup.find_all('div','feed-post-body-title'):
        try:
            link = get_link(news) # pegar o link
        
            title = get_title(news) # pegar o título
        
            r2 = requests.get(link) # entrar no link
            soup2 = BeautifulSoup(r2.text, 'lxml')
        
            classes_secundarias = soup2.find_all(class_='entities__list-item') # classes adicionais 
            cs = get_class(categoria, classes_secundarias)       
        
            conteudo = soup2.find_all('p', 'content-text__container') # texto da noticia
            text = get_conteudo(conteudo)

            # salvar em csv
            df = df.append({'Título':title, 'Classes':cs, 'Link':link, 'Conteúdo':text}, ignore_index = True)
            count_news += 1   
        except:
            pass 

    # vai para a próxima página
    next_page = soup.find(class_='load-more')
    url = next_page.find('a').get('href')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

# cria o arquivo csv com as saídas
df.to_csv('C:/Users/Márcio/Downloads/PEDRO/Projeto/g1dataset.csv')    


# https://scikit-learn.org/stable/modules/feature_extraction.html
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
# https://scikit-learn.org/stable/modules/multiclass.html
# https://realpython.com/nltk-nlp-python/
# https://scikit-learn.org/stable/modules/cross_validation.html
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html