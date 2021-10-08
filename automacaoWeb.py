from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

#01 Obtendo cotação do Dolar
navegador = webdriver.Chrome("chromedriver.exe") #Criando um navegador Chrome
navegador.get("https://www.google.com/")#Acessando site especificado

#Buscando a barra de pesquisa do google pelo xpath
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("Cotação do Dólar")#digitando o termo
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)#Acessando a tecla Enter
#Capturando a cotação do dolar pelo xpath e pegando o atributo data-value do HTML da página
cotacao_dolar = navegador.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(f'COTAÇÃO DO DOLAR: R${cotacao_dolar}')

#02 Obtendo a cotação do Euro
navegador.get("https://www.google.com/")
#Buscando a barra de pesquisa do google pelo xpath
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("Cotação do Euro")#digitando o termo
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)#Acessando a tecla Enter
#Capturando a cotação do dolar pelo xpath e pegando o atributo data-value do HTML da página
cotacao_euro = navegador.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(f'COTAÇÃO DO EURO: R${cotacao_euro}')

#03 Obtendo a cotação do Ouro
#Entrando no site melhorcambio.com
navegador.get("https://www.melhorcambio.com/ouro-hoje")
#Pegando a cotação do ouro pelo xpath e coletando a informação do atributo 'valur' do HTML
cotacao_ouro = navegador.find_element_by_xpath('//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(',', '.')#Correção de padronização numérica
print(cotacao_ouro)

#04 Acessando e lendo a base de dados
tabela = pd.read_excel("Produtos.xlsx")

#05 Atualizando a cotação
#O comando loc irá localizar a linha e a coluna passadas como parametro
#O primeiro parametro é a linha, nesse caso irá pegar todas as linhas na qual
#a coluna 'Moeda' tiver o valor da moeda pretendida
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)#casting pois a informação pode vir como string do HTML
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)#casting
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)#casting

#Atualizando preço de compra: Preço de Compra = Preço Original * Cotação
tabela["Preço Base Reais"] = tabela["Preço Base Original"] * tabela["Cotação"]

#Atualizando o preço de venda: Preço de Venda = Preço de Compra * Margem
tabela["Preço Final"] = tabela["Preço Base Reais"] * tabela["Margem"]

#06 Exportando relatório atualizado
tabela.to_excel("Produtos novo.xlsx", index=False) 
navegador.quit()#Fecha o browser
#O primeiro parametro é o nome do arquivo, se for igual o original irá substituir
#index = coluna criada pelo python para identificar as linhas da tabela
##display(tabela)