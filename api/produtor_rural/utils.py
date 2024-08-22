def validate_cpf(cpf: str) -> bool:
    if len(cpf) != 14:
        return False
    cpf = cpf.replace('.', '').replace('-', '')
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    def calcular_digito(cpf: str, posicoes: int) -> int:
        soma = sum(int(cpf[i]) * (posicoes - i) for i in range(posicoes - 1))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    digito1 = calcular_digito(cpf, 10)
    digito2 = calcular_digito(cpf, 11)

    return cpf[-2:] == f'{digito1}{digito2}'

def validate_cnpj(cnpj: str) -> bool:
    if len(cnpj) != 18:
        return False
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj) != 14 or not cnpj.isdigit():
        return False

    def calcular_digito(cnpj: str, pesos: list) -> int:
        soma = sum(int(cnpj[i]) * peso for i, peso in enumerate(pesos))
        resto = (soma % 11)
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    digito1 = calcular_digito(cnpj, pesos1)
    digito2 = calcular_digito(cnpj + str(digito1), pesos2)

    return cnpj[-2:] == f'{digito1}{digito2}'
