import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Cria a tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        name TEXT,
        change_24h TEXT
    )
''')
conn.commit()

# Configura o navegador
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acessa o site
driver.get('https://coinmarketcap.com/')

# Aguarda até que o tbody da tabela esteja presente
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody"))
)

sort_button = driver.find_element(By.XPATH, "//table//thead//tr//th[6]//div//div//p")
sort_button.click()

def capture_data():
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")

    for index, row in enumerate(rows):
        if index >= 5:
            break

        try:
            # Nome da moeda
            name = row.find_element(By.XPATH, ".//td[3]//div//a//span//div//div//p").text

            # Percentual de crescimento em 24h (coluna 5)
            change_24h = row.find_element(By.XPATH, ".//td[6]//span").text

            #----------BD----------------

            # Busca o último valor registrado para a moeda
            cursor.execute('''
                            SELECT change_24h FROM coins
                            WHERE name = ?
                            ORDER BY timestamp DESC
                            LIMIT 1
                        ''', (name,))
            result = cursor.fetchone()

            # Só insere se não existe ou se mudou o valor
            if not result or result[0] != change_24h:
                cursor.execute("INSERT INTO coins (name, change_24h) VALUES (?, ?)", (name, change_24h))
                conn.commit()
                print(f"[INSERIDO] {name}: {change_24h}")
            else:
                print(f"[IGNORADO] {name}: sem mudança")

            print(f"{name}: {change_24h}")
        except Exception as e:
            continue


while True:
    print('-' * 30)
    time.sleep(10)
    capture_data()
