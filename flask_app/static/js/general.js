document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        $(function(){ 
            $('.nav-tabs a').on('click', function (e) {
                e.preventDefault();
                $(this).tab('show');
            });  
          });
        // var time = false;
        // var temperatures = false;
        // var humidities = false;
        // var chartData = false;
        // var autoControl = true;
        // var timeFormat = 'hh:mm';

        // var tempAtualElement = document.getElementById("temp-atual-value")
        // var humiAtualElement = document.getElementById("humi-atual-value")
        // var humistateAtualElement = document.getElementById("humistate-atual-value")

        // CADASTRO ELEMENTS
        var cadastroModeloElement = document.getElementById("modelo-input")
        var cadastroAnoElement = document.getElementById("ano-input")
        var cadastroPlacaElement = document.getElementById("placa-input")
        var cadastrarButton = document.getElementById("cadastrar-button")
        var cadastroEstadoLiberadoOnRadio = document.getElementById("estado-on-input")
        var cadastroEstadoManutencaoOffRadio = document.getElementById("estado-off-input")

        cadastrarButton.addEventListener('click', car_register);

        function car_register(){
            //window.alert("Valores Incorretos!\n\nUmidade só varia de 0 a 100% e a variação de 0 a 5%")
            $.ajax({
                type: 'POST',
                url: '/car-register',
                dataType: 'json',
                data: JSON.stringify({
                    "modelo": cadastroModeloElement.value,
                    "ano": cadastroAnoElement.value,
                    "placa": cadastroPlacaElement.value,
                    "estado": cadastroEstadoLiberadoOnRadio.checked
                }),
                contentType: 'application/json',
                success: function (data) {
                    if (data.status=="Error"){
                        window.alert(
                            `Erro!\n\n${data.msg}`
                        )
                    }else{
                        window.alert(
                            `Sucesso!\n\n${data.msg}`
                        )
                    }
                }
            })
        }

        // VEICULOS CADASTRADOS ELEMENTS
        var tabVeiculosCadastrados = document.getElementById("ex3-tab-3")
        var dropdownFiltros = document.getElementById("filtros");
        var all_cars;
        var inicio=[];
        var termino=[]
        var reservar=[]
        var cancelar=[]
        var inicioInput=[]
        var terminoInput=[]
        var btnReserva=[]
        var btnCancela=[]

        tabVeiculosCadastrados.addEventListener('click', showCars)
        dropdownFiltros.addEventListener('change', showCars)

        function showCars(){
            $.ajax({
                        url: '/cars-get',
                        type: 'GET',
                        dataType: 'json',
                        //data: JSON.stringify({'art_name': modalTextNovaArte.value}),
                        contentType: 'application/json',
                        success: function (data) {
                            all_cars = data.cars
                            renderCars(data)
                        },
                        async: false
            }); 
        }

        function renderCars(data){
            var filter = dropdownFiltros.value;
            const cars = []
            for (var i = 0; i < data.cars.length; i++) {
                if (filter=="Alugado"){
                    if (data.cars[i].alugado == "Veículo reservado"){
                        cars.push(data.cars[i])
                    }
                }else if(filter=="NaoAlugado"){
                    if (data.cars[i].alugado != "Veículo reservado"){
                        cars.push(data.cars[i])
                    }
                }else if(filter=="Manutencao"){
                    if (data.cars[i].estado != "Liberado"){
                        cars.push(data.cars[i])
                    }
                }else{
                    cars.push(data.cars[i])
                }
            }
            
            renderRows(cars)

            inicio=[];
            termino=[]
            reservar=[]
            cancelar=[]
            inicioInput=[]
            terminoInput=[]
            btnReserva=[]
            btnCancela=[]

            for (var i = 0; i < cars.length; i++) {
                inicio.push(document.getElementById(`inicio${cars[i].id}`))
                termino.push(document.getElementById(`termino${cars[i].id}`))
                reservar.push(document.getElementById(`reservar${cars[i].id}`))
                cancelar.push(document.getElementById(`cancelar${cars[i].id}`))
                
                inicioInput.push(document.getElementById(`inicioreserva${cars[i].id}`))
                terminoInput.push(document.getElementById(`terminoreserva${cars[i].id}`))
                inicioInput[i].valueAsDate = new Date();
                terminoInput[i].valueAsDate = new Date();

                btnReserva.push(document.getElementById(`btnreserva${cars[i].id}`))
                btnCancela.push(document.getElementById(`btncancelar${cars[i].id}`))

                btnCancela[i].addEventListener('click', cancelar_reserva)
                btnReserva[i].addEventListener('click', salvar_reserva)

                if (cars[i].inicio_aluguel == "-" || cars[i].termino_aluguel == "-"){
                    inicio[i].style.display = 'none'
                    termino[i].style.display = 'none'
                    reservar[i].style.display = 'block'
                    cancelar[i].style.display = 'none'
                }else{
                    inicio[i].style.display = 'block'
                    termino[i].style.display = 'block'
                    reservar[i].style.display = 'none'
                    cancelar[i].style.display = 'block'
                }
            }
            
        }

        function cancelar_reserva(){
            var index = parseInt(this.id.slice(this.id.length - 1))
            $.ajax({
                type: 'POST',
                url: '/cancelar-reserva',
                dataType: 'json',
                data: JSON.stringify({
                    "id": index,
                }),
                contentType: 'application/json',
                success: function (data) {
                    if (data.status=="Error"){
                        window.alert(
                            `Erro!\n\n${data.msg}`
                        )
                    }else{
                        window.alert(
                            `Sucesso!\n\n${data.msg}`
                        )
                        showCars()
                    }
                }
            })
        }

        function salvar_reserva(){
            var index = parseInt(this.id.slice(this.id.length - 1))
            $.ajax({
                type: 'POST',
                url: '/reservar',
                dataType: 'json',
                data: JSON.stringify({
                    "id": index,
                    "inicio": inicioInput[index-1].value,
                    "termino": terminoInput[index-1].value
                }),
                contentType: 'application/json',
                success: function (data) {
                    if (data.status=="Error"){
                        window.alert(
                            `Erro!\n\n${data.msg}`
                        )
                    }else{
                        window.alert(
                            `Sucesso!\n\n${data.msg}`
                        )
                        showCars()
                    }
                }
            })
        }

    }
}



        // var baseUrl = '@Url.Content("~/mvc")';
        // console.log(baseUrl)

        // function change_auto_control_off(){
        //     $.ajax({
        //         type: 'POST',
        //         url: '/post-update-auto-control',
        //         dataType: 'json',
        //         data: JSON.stringify({
        //             "auto_control": false,
        //         }),
        //         contentType: 'application/json',
        //         success: function () {
        //             get_last_status();
        //         }
        //     })
        // }

        // function get_data(){
        //     $.ajax({
        //                     url: '/get-data',
        //                     type: 'GET',
        //                     dataType: 'json',
        //                     //data: JSON.stringify({'art_name': modalTextNovaArte.value}),
        //                     contentType: 'application/json',
        //                     success: function (data) {
        //                         time = split_time(data["time"]);
        //                         temperatures = data["temperature"];
        //                         humidities = data["humidity"]
        //                         humidifier_state = data["humidifier_state"]
        //                     },
        //                     async: false
        //                 }); 
        // }

        // function get_last_status(){
        //     $.ajax({
        //                     url: '/get-last-status',
        //                     type: 'GET',
        //                     dataType: 'json',
        //                     //data: JSON.stringify({'art_name': modalTextNovaArte.value}),
        //                     contentType: 'application/json',
        //                     success: function (data) {
        //                         autoControl = data["auto_control"];
        //                         if (autoControl == false){
        //                             umidadeDesejadaElement.disabled = true;
        //                             variacaoMaximaElement.disabled = true;
        //                             updateInfoButton.disabled = true;
        //                             ligarDesligarHumiLabel.style.display = 'block';
        //                             ligarDesligarHumiButton.style.display = 'block';
        //                             autoControlOffRadio.checked = true;
        //                         }else if (autoControl == true){
        //                             umidadeDesejadaElement.disabled = false;
        //                             variacaoMaximaElement.disabled = false;
        //                             updateInfoButton.disabled = false;
        //                             ligarDesligarHumiLabel.style.display = 'none';
        //                             ligarDesligarHumiButton.style.display = 'none';
        //                             autoControlOnRadio.checked = true;
        //                         }
        //                         tempAtualElement.innerHTML = `Temperatura: ${data["temperature"]}°C`;
        //                         humiAtualElement.innerHTML = `Umidade: ${data["humidity"]}%`;
        //                         humidifier_state = data["humidifier_state"]
        //                         if (humidifier_state==1){
        //                             humistateAtualElement.innerHTML = `Umidificador Ligado`;
        //                             ligarDesligarHumiButton.innerText = `Desligar`
        //                         }else if (humidifier_state==0){
        //                             humistateAtualElement.innerHTML = `Umidificador Desligado`                            ;
        //                             ligarDesligarHumiButton.innerText = `Ligar`
        //                         }
        //                     },
        //                     async: false
        //                 }); 
        // }

        // function get_set_point(){
        //     $.ajax({
        //                     url: '/get-set-point',
        //                     type: 'GET',
        //                     dataType: 'json',
        //                     //data: JSON.stringify({'art_name': modalTextNovaArte.value}),
        //                     contentType: 'application/json',
        //                     success: function (data) {
        //                         umidadeDesejadaElement.value = data["humidity_set_point"];
        //                         variacaoMaximaElement.value = data["humidity_deviation"];
        //                     },
        //                     async: false
        //                 }); 
        // }


        // function split_time(tempo){
        //     let x = new Date(tempo[0])
        //     var t2 = new Array();
        //     for (var i = 0; i < tempo.length; i++) {
        //         t = new Date(tempo[i])
        //         t2.push(moment().hour(t.getUTCHours()).minute(t.getUTCMinutes()).format(timeFormat));
        //     }
        //     return(t2)
        // }

        // function newDateString(hours, minutes, seconds) {
        //     return moment().hour(hours).minute(minutes).second(seconds).format(timeFormat);
        //     }

        // function update_chart(){
        //     get_data();
        //     Temp_chart.data.labels = time
        //     Temp_chart.data.datasets[0].data = temperatures;
            
        //     Hum_chart.data.labels = time
        //     Hum_chart.data.datasets[0].data = humidities;
            
        //     Temp_chart.update();   
        //     Hum_chart.update();
        // }

        // get_data();
        // get_set_point();
        // get_last_status();
        // setInterval(update_chart, 30000)
        // setInterval(get_last_status, 5000)