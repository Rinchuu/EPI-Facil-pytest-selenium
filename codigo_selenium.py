from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException

# Abrir o navegador
navegador = webdriver.Chrome()

# Acessar um site
navegador.get("http://127.0.0.1:8000/")

# Colocar o navegador em tela cheia
navegador.maximize_window()

# Selecionar o botão de login
botao_verde = navegador.find_element("class name", "login-btn")
botao_verde.click()

# Aguardar o carregamento da página de login
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "email")))

# Preencher o formulário de login
navegador.find_element(By.NAME, "email").send_keys("pythonimpressionador@gmail.com")
navegador.find_element(By.NAME, "senha").send_keys("123456")

# Clicar no botão de login
botao_quero_clicar = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "login-btn"))
)
botao_quero_clicar.click()

# Espera para garantir que o login foi feito
time.sleep(5)

# Abrir nova guia para cadastro de EPI
navegador.execute_script("window.open('');")
abas = navegador.window_handles
navegador.switch_to.window(abas[1])

# Acessar o site de cadastro de EPIs
navegador.get("http://127.0.0.1:8000/epis/cadastro/")

# Espera dinâmica para preencher o formulário de EPI
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "nome"))).send_keys("Capacete de Segurança")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "quantidade"))).send_keys("100")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "valor"))).send_keys("50.00")

# Clicar no botão de cadastro de EPI
botao_cadastrar_epi = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "login-btn"))
)
botao_cadastrar_epi.click()

# Espera para garantir que o EPI foi cadastrado
WebDriverWait(navegador, 10).until(EC.url_changes("http://127.0.0.1:8000/epis/cadastro/"))
time.sleep(5)

# Abrir nova guia para registro de ação
navegador.execute_script("window.open('');")
abas = navegador.window_handles
navegador.switch_to.window(abas[2])

# Acessar a página de registro de ação
navegador.get("http://127.0.0.1:8000/epis/registrar_acao/")

navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Espera dinâmica para preencher o formulário de registro de ação
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "nome_equipamento"))).send_keys("Capacete de Segurança")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "usuario"))).send_keys("Lira")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "data_emprestimo"))).send_keys("2024-11-30 08:00")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "data_prevista_devolucao"))).send_keys("2024-12-07 08:00")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "status"))).send_keys("emprestado")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "condicao_emprestimo"))).send_keys("Equipamento em bom estado.")
WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.NAME, "observacao_devolucao"))).send_keys("testei e sai correndo")

# Esperar até o botão estar visível na tela

botao_registrar_acao = WebDriverWait(navegador, 10).until(
    EC.visibility_of_element_located((By.NAME, "save-button"))  # Substitua "id_do_botao" com o ID real do botão
)

# Role até o botão usando JavaScript
# Rolar até o botão usando JavaScript
navegador.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });", botao_registrar_acao)

time.sleep(1)

# Clicar no botão
botao_registrar_acao.click()

# Espera para garantir que a ação foi registrada
WebDriverWait(navegador, 10).until(EC.url_changes("http://127.0.0.1:8000/epis/listar_acoes/"))
time.sleep(5)
# Fechar o navegador

navegador.quit()

