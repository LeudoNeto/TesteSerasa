document.addEventListener("DOMContentLoaded", function() {
    var modalCriarProdutorRural = document.querySelector('#modalCriarProdutorRural');
    var salvarProdutorRural = modalCriarProdutorRural.querySelector('#salvarProdutorRural');
    var formCriarProdutorRural = document.querySelector('#formCriarProdutorRural');

    var editarProdutorRuralButtons = document.querySelectorAll('#editarProdutorRural');
    var modalEditarProdutorRural = document.querySelector('#modalEditarProdutorRural');
    var formEditarProdutorRural = document.querySelector('#formEditarProdutorRural');
    var salvarEditarProdutorRural = modalEditarProdutorRural.querySelector('#salvarProdutorRural');

    var excluirProdutorRuralButtons = document.querySelectorAll('#excluirProdutorRural');

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvarProdutorRural.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

        let formData = new FormData(formCriarProdutorRural);
        if (formCriarProdutorRural.checkValidity()) {
            if (!validateCpfCnpj(formData.get('cpf_cnpj'))) {
                swal.fire({
                    title: "CPF/CNPJ inválido",
                    text: "Verifique o CPF/CNPJ informado e tente novamente.",
                    icon: "error"
                });
                return;
            }
            if (!validateAreas(formData)) {
                swal.fire({
                    title: "Áreas inválidas",
                    text: "A área total deve ser maior ou igual à soma das áreas agricultável e de vegetação.",
                    icon: "error"
                });
                return;
            }
            swal.fire({
                title: "Produtor Rural validado com sucesso!",
                text: "Clique em 'Confirmar' para salvar o produtor rural.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                formData.append('usa_cpf', formData.get('cpf_cnpj').length === 14);
                formData.append('area_total_hectares', formData.get('area_total_hectares').replace(/\D/g, '')/100);
                formData.append('area_agricultavel_hectares', formData.get('area_agricultavel_hectares').replace(/\D/g, '')/100);
                formData.append('area_vegetacao_hectares', formData.get('area_vegetacao_hectares').replace(/\D/g, '')/100);

                let formJSON = {};
                formData.forEach((value, key) => formJSON[key] = value);

                if (result.isConfirmed) {
                    fetch("/api/produtor_rural/", {
                        headers: {
                            "X-CSRFToken": csrf_token,
                            "Content-Type": "application/json"
                        },
                        method: "POST",
                        body: JSON.stringify(formJSON)
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produtor Rural salvo com sucesso!",
                                icon: "success"
                            }).then(() => {
                                window.location.reload();
                            });
                        }
                        else {
                            return response.text().then(data => {
                                swal.fire({
                                    title: "Ocorreu um erro",
                                    text: data,
                                    icon: "error"
                                });
                            });
                        }
                    })
                }
            });
        } else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error",
            })
        }

    });

    // preencher formulário de edição com dados do produtor rural
    editarProdutorRuralButtons.forEach(button => {
        button.addEventListener('click', function() {

            swal.fire({
                title: "Carregando dados do Produtor Rural",
                icon: "info"
            });

            let produtor_id = button.getAttribute('data-id');
            fetch(`/api/produtor_rural/${produtor_id}/`)
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        for (const key in data) {
                            let input = formEditarProdutorRural.querySelector(`[name=${key}]`);
                            if (input) {
                                if (input.type === 'checkbox') {
                                    input.checked = data[key];
                                } else {
                                    input.value = data[key];
                                }
                            }
                        }
                        salvarEditarProdutorRural.dataset.id = produtor_id;
                        swal.close();
                        
                    });
                }
                else {
                    return response.text().then(data => {
                        swal.fire({
                            title: "Ocorreu um erro",
                            text: data,
                            icon: "error"
                        });
                    });
                }
            });
            
        });
    });

    salvarEditarProdutorRural.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

        let formData = new FormData(formEditarProdutorRural);
        if (formEditarProdutorRural.checkValidity()) {
            if (!validateCpfCnpj(formData.get('cpf_cnpj'))) {
                swal.fire({
                    title: "CPF/CNPJ inválido",
                    text: "Verifique o CPF/CNPJ informado e tente novamente.",
                    icon: "error"
                });
                return;
            }
            if (!validateAreas(formData)) {
                swal.fire({
                    title: "Áreas inválidas",
                    text: "A área total deve ser maior ou igual à soma das áreas agricultável e de vegetação.",
                    icon: "error"
                });
                return;
            }
            swal.fire({
                title: "Produtor Rural validado com sucesso!",
                text: "Clique em 'Confirmar' para salvar o produtor rural.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                formData.append('usa_cpf', formData.get('cpf_cnpj').length === 14);
                formData.append('area_total_hectares', formData.get('area_total_hectares').replace(/\D/g, '')/100);
                formData.append('area_agricultavel_hectares', formData.get('area_agricultavel_hectares').replace(/\D/g, '')/100);
                formData.append('area_vegetacao_hectares', formData.get('area_vegetacao_hectares').replace(/\D/g, '')/100);

                let formJSON = {};
                formData.forEach((value, key) => formJSON[key] = value);

                let produtor_id = salvarEditarProdutorRural.getAttribute('data-id');
                if (result.isConfirmed) {
                    fetch(`/api/produtor_rural/${produtor_id}/`, {
                        method: "PUT",
                        headers: {
                            "X-CSRFToken": csrf_token,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(formJSON)
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produtor Rural editado com sucesso!",
                                icon: "success"
                            }).then(() => {
                                window.location.reload();
                            });
                        }
                        else {
                            return response.text().then(data => {
                                swal.fire({
                                    title: "Ocorreu um erro",
                                    text: data,
                                    icon: "error"
                                });
                            });
                        }
                    })
                }
            });
        } else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error",
            })
        }

    });


    excluirProdutorRuralButtons.forEach(button => {
        button.addEventListener('click', function() {
            let produtor_id = button.getAttribute('data-id');
            swal.fire({
                title: "Tem certeza que deseja excluir o Produtor Rural?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch("/api/produtor_rural/" + produtor_id, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf_token
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produtor Rural excluído com sucesso!",
                                icon: "success"
                            }).then(() => {
                                button.closest('tr').remove();
                            });
                        }
                        else {
                            return response.text().then(data => {
                                swal.fire({
                                    title: "Ocorreu um erro",
                                    text: data,
                                    icon: "error"
                                });
                            });
                        }
                    });
                }
            });
        });
    });


});

function formatCpfCnpj(input) {
    let value = input.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (value.length <= 11) {
        // CPF format
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    } else {
        // CNPJ format
        value = value.replace(/^(\d{2})(\d)/, '$1.$2');
        value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
        value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
        value = value.replace(/(\d{4})(\d)/, '$1-$2');
    }
    input.value = value;
}

function validateCpfCnpj(value) {
    // Remove caracteres não numéricos
    value = value.replace(/\D/g, '');
    
    if (value.length === 11) {
        return validateCPF(value);
    } else if (value.length === 14) {
        return validateCNPJ(value);
    } else {
        return false;
    }
}

function validateCPF(cpf) {
    // Verifique se os dígitos são iguais
    if (/^(\d)\1+$/.test(cpf)) return false;
    
    let sum = 0;
    let remainder;

    // Valida o primeiro dígito
    for (let i = 1; i <= 9; i++) {
        sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.substring(9, 10))) return false;

    // Valida o segundo dígito
    sum = 0;
    for (let i = 1; i <= 10; i++) {
        sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.substring(10, 11))) return false;

    return true;
}

function validateCNPJ(cnpj) {
    // Verifique se os dígitos são iguais
    if (/^(\d)\1+$/.test(cnpj)) return false;

    let length = cnpj.length - 2;
    let numbers = cnpj.substring(0, length);
    let digits = cnpj.substring(length);
    let sum = 0;
    let pos = length - 7;

    for (let i = length; i >= 1; i--) {
        sum += numbers.charAt(length - i) * pos--;
        if (pos < 2) pos = 9;
    }
    let result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
    if (result !== parseInt(digits.charAt(0))) return false;

    length = length + 1;
    numbers = cnpj.substring(0, length);
    sum = 0;
    pos = length - 7;

    for (let i = length; i >= 1; i--) {
        sum += numbers.charAt(length - i) * pos--;
        if (pos < 2) pos = 9;
    }
    result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
    if (result !== parseInt(digits.charAt(1))) return false;

    return true;
}

function formatArea(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, '');
    valor = (valor / 100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
    input.value = valor;
}

function validateAreas(formData) {
    let area_total_hectares = formData.get('area_total_hectares').replace(/\D/g, '')/100;
    let area_agricultavel_hectares = formData.get('area_agricultavel_hectares').replace(/\D/g, '')/100;
    let area_vegetacao_hectares = formData.get('area_vegetacao_hectares').replace(/\D/g, '')/100;

    return area_total_hectares >= area_agricultavel_hectares + area_vegetacao_hectares;
}