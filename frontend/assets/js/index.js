document.addEventListener("DOMContentLoaded", function() {
    var totalFazendas = document.querySelector("#totalFazendas");
    var totalFazendasHectares = document.querySelector("#totalFazendasHectares");

    var pizzaEstadosChart = document.querySelector("#pizzaEstadosChart");
    var estadosTotalText = document.querySelector("#estadosTotalText");

    var pizzaCulturasChart = document.querySelector("#pizzaCulturasChart");
    var culturasTotalText = document.querySelector("#culturasTotalText");

    var pizzaUsoSoloChart = document.querySelector("#usoSoloChart");
    var usoSoloTotalText = document.querySelector("#usoSoloTotalText");

    fetch('/api/dashboard/')
    .then(response => {
        if (response.ok) {
            return response.json().then(data => {
                totalFazendas.innerHTML = data.total_fazendas;
                totalFazendasHectares.innerHTML = data.total_hectares;

                let total_estados = 0;
                for (let estado in data.estados_pizza) {
                    total_estados += data.estados_pizza[estado];
                }
                estadosTotalText.innerHTML = Object.keys(data.estados_pizza).length; // estados únicos
                makePizzaChart(pizzaEstadosChart, data.estados_pizza, total_estados);

                let total_culturas = 0;
                for (let cultura in data.culturas_pizza) {
                    total_culturas += data.culturas_pizza[cultura];
                }
                culturasTotalText.innerHTML = total_culturas;
                makePizzaChart(pizzaCulturasChart, data.culturas_pizza, total_culturas);

                let total_uso_solo = 0;
                for (let uso_solo in data.uso_solo_pizza) {
                    total_uso_solo += data.uso_solo_pizza[uso_solo];
                }
                usoSoloTotalText.innerHTML = total_uso_solo;
                makePizzaChart(pizzaUsoSoloChart, data.uso_solo_pizza, total_uso_solo);
            });
        }
        else {
            return response.json().then(data => {
                swal.fire({
                    title: data.erro,
                    text: data.detalhes,
                    icon: "error"
                });
            });
        }
        
    })
      

    if (document.documentElement.getAttribute('data-theme') == 'light') {
        var cardColor = config.colors.white;
        var headingColor = config.colors.headingColor;
    }
    else {
        var cardColor = config.colors.dark;
        var headingColor = config.colors.white;
    }
    function makePizzaChart(chart, data, total) {
        // Pizza Chart
        // --------------------------------------------------------------------
        pizzaChartConfig = {
            chart: {
                height: 165,
                width: 130,
                type: 'donut'
            },      
            labels: Object.keys(data),
            series: Object.values(data),
            colors:['#FFC107', '#28A745', '#007BFF', '#DC3545', '#17A2B8',
                    '#6610f2', '#6f42c1', '#e83e8c', '#fd7e14', '#20c997'],
            stroke: {
                width: 5,
                colors: cardColor
            },
            dataLabels: {
            enabled: false,
            formatter: function (val, opt) {
                return parseInt(val) + '%';
            }
            },
            legend: {
            show: false
            },
            grid: {
            padding: {
                top: 0,
                bottom: 0,
                right: 15
            }
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '75%',
                        labels: {
                            show: true,
                            value: {
                                fontSize: '1.5rem',
                                fontFamily: 'Public Sans',
                                color: headingColor,
                                offsetY: -15,
                                formatter: function (val) {
                                    return parseInt((val*100)/total) + '%';
                                }
                            },
                            name: {
                            offsetY: 20,
                            fontFamily: 'Public Sans'
                            },
                            total: {
                                show: true,
                                fontSize: '0.8125rem',
                                color: config.colors.primary,
                                label: Object.keys(data)[0],
                                formatter: function (w) {
                                    return parseInt((Object.values(data)[0]*100)/total) + "%";
                                }
                            }
                        }
                    }
                }
            }
        };
        if (typeof chart !== undefined && chart !== null) {
            let pizzaChart = new ApexCharts(chart, pizzaChartConfig);
            pizzaChart.render();
        }
    }
      
});