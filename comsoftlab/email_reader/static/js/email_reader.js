const WS_URL = 'ws://' + window.location.host + '/ws/email_reader/'

var email_selector = document.querySelector('#email_selector')
var table = document.querySelector('#messages_table')
var progressbar = document.querySelector('#progressbar')
var progressbar_count = document.querySelector('#progress_count')


email_selector.addEventListener("change", (e) => {
    // При новом выборе почты, обнуляем всю таблицу и прогресс-бар
    table.innerHTML = ""
    progressbar.style.width = "0%"
    progressbar_count.innerHTML = 0

    // Формируем корректный URL подключения по вебсокету
    var service = e.target.options[e.target.selectedIndex].dataset.service
    var email_ws_url = WS_URL + e.target.value + "/" + service
    var ws = new WebSocket(email_ws_url)

    // Обрабатываем полученный ответ
    ws.onmessage = (e) => {
        var sent_data = JSON.parse(e.data)
        // Если тело ответа содержит в себе информацию о сообщении, добавляем его в таблицу
        if (sent_data.message) {
            // Формируем HTML-разметку строки
            var row_html = `<tr>
                                    <th scope="row">${sent_data.message.email_from}</th>
                                    <th>
                                        <a href="${'/message/' + sent_data.message.service + "/"+ sent_data.message.uid}">
                                            ${sent_data.message.subject}                        
                                        </a>
                                    </th>
                                    <th>${(sent_data.message.text).substring(0, 100)}</th>
                                    <th>${sent_data.message.date_sent}</th>  
                                    <th>${sent_data.message.files.length}</th>  
                             </tr>`;
            // Указываем актуальную информацию в прогресс-баре и добавляем строку в таблицу
            progressbar_count.innerText = 'Загрузка: ' + sent_data.count + "/" + sent_data.total_messages
            progressbar.style.width = (sent_data.count / sent_data.total_messages) * 100 + '%'
            table.innerHTML += row_html
        }
        // Если сообщение в теле ответа не пришло, значит все еще происходит загрузка, отображаем ее в прогресс-баре
        else {
            progressbar_count.innerText = "Прочитано писем " + sent_data.progress
        }
    }
})