import requests
from bs4 import BeautifulSoup
import threading

def scrape_mercado_libre(precio_lap,cantidad):
   
    
    # Realizar la solicitud HTTP a la página web
    url = requests.get('https://listado.mercadolibre.com.mx/laptops#D[A:laptops]')
    soup = BeautifulSoup(url.content, 'html.parser')

    # Buscar todos los elementos que contienen los títulos y enlaces de las laptops
    elementos_a = soup.find_all('div', class_='ui-search-item__group ui-search-item__group--title')

    # Encontrar todos los elementos que contengan la clase principal de precio
    precios = soup.find_all('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript')

    contador = 1

    # Iterar a través de los elementos encontrados y combinar los enlaces con los precios
    for element_h2, precio in zip(elementos_a, precios):
        elemento_a = element_h2.find('a')  # Obtener el enlace de la laptop
        precio_texto = precio.get('aria-label')  # Obtener el precio desde aria-label

        if elemento_a and precio_texto:
            # Convertir el texto de precio a número entero
            precio_entero = int(''.join(filter(str.isdigit, precio_texto)))
            
            # Verificar si el precio es menor a 5000
            if precio_entero < precio_lap and contador <= cantidad:
                contador += 1
                # Imprimir el precio y el enlace
                print("MERCADO LIBRE")
                print(f"Precio: ${precio_entero}, URL: {elemento_a['href']}")

    print("Finalizado para Mercado Libre")

def scrape_infotec(precio_lap,cantidad):
    
    # Realizar la solicitud HTTP a la página web
    url = requests.get('https://www.infotec.com.pe/3-laptops-y-notebooks')
    soup = BeautifulSoup(url.content, 'html.parser')

    contador = 1

    #Se obtiene donde se encuentra los precios
    elementos_a = soup.find_all('div', class_='product-price-and-shipping')

    for element_h2 in elementos_a:
        elemento_a = element_h2.find('a')  # Obtener el enlace de la laptop
        precio_texto = element_h2.find('span').get_text().strip() # Obtener el precio
        if elemento_a and precio_texto:
            # Convertir el texto de precio a número entero
            precio_entero = int(''.join(filter(str.isdigit, precio_texto)))
            
            # Verificar si el precio es menor a 1300 soles
            if precio_entero < precio_lap and contador <= cantidad:
                contador += 1
                # Imprimir el precio y el enlace}
                print("INFOTEC")
                print(f"Precio en soles: ${precio_entero}, URL: {elemento_a['href']}")

    print("Finalizado para Infotec")



# Crear hilos para ejecutar cada función de scraping

thread_infotec = threading.Thread(target=scrape_infotec, args=(1300, 5, )) #1300 soles peruanos son equivalente a $6800 pesos mexicanos
thread_mercado_libre = threading.Thread(target=scrape_mercado_libre , args=(7000, 5, ))

# Iniciar los hilos
thread_mercado_libre.start()
thread_infotec.start()

# Esperar a que ambos hilos terminen

thread_mercado_libre.join()
thread_infotec.join()

print("Scraping completado.")


