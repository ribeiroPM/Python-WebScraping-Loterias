import json
from os import system

def import_arquivo():
	try:
		arq = open("resultados005427.json")
	except:
		pass
	else:
		arquivo_json = json.loads(arq.read())
		arq.close()
	return arquivo_json

def verifica_ausencias(n_concursos):
	quantidade_concursos = 2652
	concursos_ausentes = []
	for x in range(1, quantidade_concursos+1):
		if str(x) not in n_concursos:
			concursos_ausentes.append(str(x))
	print(', '.join(concursos_ausentes) if len(concursos_ausentes)>0 else "Não há concursos ausentes")

dados_dos_concursos = import_arquivo()
num_concursos = dados_dos_concursos.keys()


def menu():
	opcoes = 'Consultar Concurso,Checar Incidencia,Sair'.split(',')
	for n, opc in enumerate(opcoes):
		print(n+1, opc)
	while True:
		try:
			escolha = int(input("Escolha uma opção: "))
		except:
			print("Valor invalido")
		else:
			if 0 < escolha < 4:
				return escolha
			else:
				print("Opcao invalida")

def consultar_concursos():
	while True:
		verifica_ausencias(num_concursos)

		num_concurso = str(input("Consultar resultado: [x p/ sair]"))
		system("cls")
		if num_concurso == "x":
			break
		try:
			res = dados_dos_concursos[num_concurso]
		except:
			print("resultado não encontrado")
		else:
			resultado = ', '.join(res[0])
			data = f"{res[1][:2]}/{res[1][2:4]}/{res[1][4:]}"
			print(f"Concurso: {num_concurso}.\nResultado: {resultado}.\nData: {data}.\n")

def verificar_insidencia():
	sair = False
	while not sair:
		dezenas_digitadas = []
		for n in range(6):
			print(f"Dezenas digitadas: {', '.join(dezenas_digitadas)}")
			dezena = input(f"Digite a {n+1}a dezena: [x p/ sair]")
			system("cls")
			if dezena == "x":
				sair = True
				break
			dezenas_digitadas.append(f"{dezena:0>2}")
		for concurso, dezenas_sorteadas in dados_dos_concursos.items():
			if ''.join(dezenas_sorteadas[0]) == ''.join(dezenas_digitadas):
				print(concurso)

def numeros_que_mais_saem():
	todas_dezenas = {x: 0 for x in range(1, 61)}
	dezenas_mais_sorteadas = [[0, 0]]
	for dezenas in dados_dos_concursos.values():
		dezenas = [int(num) for num in dezenas[0]]
		for dezena in dezenas:
			todas_dezenas[dezena] += 1
			if todas_dezenas[dezena] > dezenas_mais_sorteadas[0][1]:
				if dezena in dezenas_mais_sorteadas:
					dezenas_mais_sorteadas.pop(dezenas_mais_sorteadas.find(dezena))
				dezenas_mais_sorteadas.insert(0, [dezena, todas_dezenas[dezena]])
	print(todas_dezenas)
	print(dezenas_mais_sorteadas)

	for k, v in todas_dezenas.items():
		print(k, v)


numeros_que_mais_saem()
exit()


while True:
	escolha = menu()
	system("cls")
	if escolha == 1:
		consultar_concursos()
	elif escolha == 2:
		verificar_insidencia()
	elif escolha == 3:
		break

	