import struct

# Defina a sequência de 6 pares de números
dados = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]

# Crie um formato binário para cada par de números (por exemplo, dois inteiros de 32 bits)
formato_binario = 'i i'

# Serialize os dados
dados_serializados = struct.pack(formato_binario * len(dados), *(numero for par in dados for numero in par))

# Para deserializar os dados, você pode usar o seguinte:
dados_deserializados = struct.unpack(formato_binario * len(dados), dados_serializados)

# Agora, dados_deserializados conterá os pares de números originalmente armazenados
print(dados_deserializados)
print(dados_serializados)
