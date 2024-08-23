document.addEventListener("DOMContentLoaded", function() {
    const modalCriarProdutorRural = document.querySelector('#modalCriarProdutorRural');
    const salvarProdutorRural = modalCriarProdutorRural.querySelector('#salvarProdutorRural');
    const formCriarProdutorRural = document.querySelector('#formCriarProdutorRural');
    
    const editarProdutorRuralButtons = document.querySelectorAll('#editarProdutorRural');
    const modalEditarProdutorRural = document.querySelector('#modalEditarProdutorRural');
    const formEditarProdutorRural = document.querySelector('#formEditarProdutorRural');
    const salvarEditarProdutorRural = modalEditarProdutorRural.querySelector('#salvarProdutorRural');
    
    const excluirProdutorRuralButtons = document.querySelectorAll('#excluirProdutorRural');
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvarProdutorRural.addEventListener('click', () => handleSave(formCriarProdutorRural, csrfToken));
    
    editarProdutorRuralButtons.forEach(button => {
        button.addEventListener('click', () => handleEdit(button, formEditarProdutorRural, salvarEditarProdutorRural, csrfToken));
    });
    
    salvarEditarProdutorRural.addEventListener('click', () => handleSave(formEditarProdutorRural, csrfToken, salvarEditarProdutorRural.getAttribute('data-id')));
    
    excluirProdutorRuralButtons.forEach(button => {
        button.addEventListener('click', () => handleDelete(button, csrfToken));
    });
});

function handleSave(form, csrfToken, produtorId = null) {
    const formData = new FormData(form);
    
    if (!form.checkValidity()) {
        showAlert("Preencha os campos obrigatórios", "error");
        return;
    }
    
    if (!validateCpfCnpj(formData.get('cpf_cnpj'))) {
        showAlert("CPF/CNPJ inválido", "error");
        return;
    }
    
    if (!validateAreas(formData)) {
        showAlert("Áreas inválidas", "error");
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
        if (result.isConfirmed) {
            submitForm(formData, csrfToken, produtorId);
        }
    });
}

function handleEdit(button, form, salvarButton, csrfToken) {
    swal.fire({
        title: "Carregando dados do Produtor Rural",
        icon: "info"
    });

    const produtorId = button.getAttribute('data-id');
    fetch(`/api/produtor_rural/${produtorId}/`)
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            populateFormWithData(form, data);
            salvarButton.dataset.id = produtorId;
            swal.close();
        })
        .catch(response => response.text().then(data => showAlert("Ocorreu um erro", "error", data)));
}

function handleDelete(button, csrfToken) {
    const produtorId = button.getAttribute('data-id');
    swal.fire({
        title: "Tem certeza que deseja excluir o Produtor Rural?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Confirmar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/api/produtor_rural/${produtorId}`, {
                method: "DELETE",
                headers: { "X-CSRFToken": csrfToken }
            })
            .then(response => response.ok ? button.closest('tr').remove() : Promise.reject(response))
            .then(() => showAlert("Produtor Rural excluído com sucesso!", "success"))
            .catch(response => response.text().then(data => showAlert("Ocorreu um erro", "error", data)));
        }
    });
}

function submitForm(formData, csrfToken, produtorId = null) {
    formatFormData(formData);
    
    const url = produtorId ? `/api/produtor_rural/${produtorId}/` : "/api/produtor_rural/";
    const method = produtorId ? "PUT" : "POST";

    const formDataJson = {};
    formData.forEach((value, key) => formDataJson[key] = value);    

    let modal = document.querySelector(produtorId ? '#modalEditarProdutorRural' : '#modalCriarProdutorRural');
    const culturas = [];
    modal.querySelectorAll('.checkbox_cultura:checked').forEach(cultura => {
        culturas.push({'nome': cultura.value});
    });
    // Adiciona as culturas ao formDataJson
    formDataJson['culturas'] = culturas;
    console.log(formDataJson)

    fetch(url, {
        method: method,
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formDataJson)
    })
    .then(response => response.ok ? swal.fire({ title: "Produtor Rural salvo com sucesso!", icon: "success" }).then(() => window.location.reload()) : Promise.reject(response))
    .catch(response => response.text().then(data => showAlert("Ocorreu um erro", "error", data)));
}

function populateFormWithData(form, data) {
    for (const key in data) {
        const input = form.querySelector(`[name=${key}]`);
        if (input) {
            input.value = data[key];
        }
    }
    
    form.querySelectorAll('.checkbox_cultura').forEach(cultura => {
        cultura.checked = data.culturas.some(c => c.nome === cultura.value);
    });
}

function formatFormData(formData) {
    formData.set('usa_cpf', formData.get('cpf_cnpj').length === 14);
    formData.set('area_total_hectares', formatArea(formData.get('area_total_hectares')));
    formData.set('area_agricultavel_hectares', formatArea(formData.get('area_agricultavel_hectares')));
    formData.set('area_vegetacao_hectares', formatArea(formData.get('area_vegetacao_hectares')));
}

function formatArea(value) {
    return (value.replace(/\D/g, '') / 100).toFixed(2);
}

function showAlert(title, icon, text = '') {
    swal.fire({ title, text, icon });
}

function validateCpfCnpj(value) {
    value = value.replace(/\D/g, '');
    return value.length === 11 ? validateCPF(value) : value.length === 14 ? validateCNPJ(value) : false;
}

function validateCPF(cpf) {
    if (/^(\d)\1+$/.test(cpf)) return false;

    const validateDigit = (weight) => {
        let sum = 0;
        for (let i = 0; i < weight.length; i++) {
            sum += parseInt(cpf[i]) * weight[i];
        }
        const remainder = (sum * 10) % 11;
        return remainder === 10 || remainder === 11 ? 0 : remainder;
    };

    return validateDigit([10, 9, 8, 7, 6, 5, 4, 3, 2]) === parseInt(cpf[9]) &&
           validateDigit([11, 10, 9, 8, 7, 6, 5, 4, 3, 2]) === parseInt(cpf[10]);
}

function validateCNPJ(cnpj) {
    if (/^(\d)\1+$/.test(cnpj)) return false;

    const validateDigit = (weight) => {
        let sum = 0;
        for (let i = 0; i < weight.length; i++) {
            sum += parseInt(cnpj[i]) * weight[i];
        }
        const remainder = (sum % 11) < 2 ? 0 : 11 - (sum % 11);
        return remainder;
    };

    const firstDigit = validateDigit([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
    const secondDigit = validateDigit([6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);

    return firstDigit === parseInt(cnpj[12]) && secondDigit === parseInt(cnpj[13]);
}

function validateAreas(formData) {
    let area_total_hectares = formData.get('area_total_hectares').replace(/\D/g, '')/100;
    let area_agricultavel_hectares = formData.get('area_agricultavel_hectares').replace(/\D/g, '')/100;
    let area_vegetacao_hectares = formData.get('area_vegetacao_hectares').replace(/\D/g, '')/100;

    return area_total_hectares >= area_agricultavel_hectares + area_vegetacao_hectares;
}

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

function formatAreaInput(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, '');
    valor = (valor / 100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
    input.value = valor;
}