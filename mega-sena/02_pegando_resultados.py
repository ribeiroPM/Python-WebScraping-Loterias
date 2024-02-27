from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, strftime
import json


# opt = webdriver.EdgeOptions()
# opt.add_argument("headless")
link = "https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx"
driver = webdriver.Edge()#options=opt)#"msedgedriver.exe")
driver.get(link)


def pega_horario():
	return f"{strftime('%H')}{strftime('%M')}{strftime('%S')}"


def aceita_cookies():
	# Função essencial para qualquer ETL envolvendo WebScrapping
	# 99% das páginas oferece cookies hoje em dia
	while True:
		try:
			botao_aceitar_cookies = driver.find_element(By.XPATH, '//*[@id="adopt-accept-all-button"]')
		except:
			sleep(2)
		else:
			botao_aceitar_cookies.click()
			break


def trata_resultado(resultado):
	# Os dados chegam na forma 102334262128
	saida = []
	for x in range(0, 12, 2):
		res = f"{resultado[x]}{resultado[x+1]}"
		saida.append(res)
	# E saem [10, 23, 34, 26, 21, 28]
	return saida


def trata_concurso_e_data(inf_concurso):
	# Exemplo Concurso 2652 (04/11/2023)
	# Separa o exemplo acima em uma tupla assim: (2652, 04112023)
	num_concurso = inf_concurso.split()[1]
	data_concurso = "".join(inf_concurso.split()[2][1:-1].split("/"))
	return num_concurso, data_concurso


aceita_cookies()
resultados = {}
a = 0
while True:
	try:
		# Pega a localização dos botões que alternam entre os concurso realizados (Anterior/Posterior)
		concurso_anterior = driver.find_element(By.XPATH, '//*[@id="wp_resultados"]/div[1]/div/div[2]/ul/li[2]/a')
		concurso_posterior = driver.find_element(By.XPATH, '//*[@id="wp_resultados"]/div[1]/div/div[2]/ul/li[3]/a')
	except:
		# Caso dê erro, provavelmente foi por ainda não ter carregado comppletamente o conteudo, então faz uma pausa de 2s
		sleep(2)
	else:
		try:
			# Tenta achar no arquivo html os dados referentes ao concurso (numero do concurso, data e numeros sorteados)
			resultado = driver.find_element(By.XPATH, '//*[@id="ulDezenas"]')
			inf_concurso = driver.find_element(By.XPATH, '//*[@id="wp_resultados"]/div[1]/div/h2/span')
		except:
			# Caso dê errado, retorna ao concurso anterior e repete a extração
			concurso_posterior.click()
		else:
			# Caso dê certo, faz o tratamendo dos dados			
			resultado = trata_resultado(resultado.text)
			inf_concurso = trata_concurso_e_data(inf_concurso.text)

			# Adiciona os dados à um dicionario
			resultados[inf_concurso[0]] = []
			resultados[inf_concurso[0]].append(resultado)
			resultados[inf_concurso[0]].append(inf_concurso[1])

		# Sai do loop ao chegar no concurso inicial
		if inf_concurso[0] == "1":
			break

		sleep(0.01)

		# Passa para o próximo concurso
		concurso_anterior.click()
driver.quit()

print(resultados)


# Caso tudo ocorra bem, exporta os resultados em um arquivo json
arq_json = open(f"resultados{pega_horario()}.json", "w")
arq_json.write(json.dumps(resultados, indent=4))
arq_json.close()
