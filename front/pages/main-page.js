const docArrayMock = [{
    name: 'doc1',
    topWords: [
        { word: "word1", weightCoef: 0.5 },
        { word: "word2", weightCoef: 0.7 }
    ],
    relevance: 0.7,
    date: '30-09-2002',
    snippet: "This is a doc snippet."
}];

class MainPage extends Page {
    buildPage() {
        const searchBar = ViewUtils.tag({
            name: "input",
            attributes: {
                type: "text",
                class: "searchbar"
            },
            eventListeners: {
                keyup: (event) => {
                    if (event.key !== 'Enter') {
                        return;
                    }
                    httpClient.post({
                        path: "docs",
                        body: {
                            query: event.target.value
                        }
                    })
                        .then(response => {
                            searchResultsPage.buildPage(response);
                            router.navigate(searchResultsPage);
                        });
                }
            }
        });

        const metricsButton = ViewUtils.tag({
            name: "button",
            attributes: {
                class: "btn-default"
            },
            eventListeners: {
                click: () => {
                    httpClient.get({
                        path: "metrics"
                    })
                        .then(response => alert(`Полнота: ${response.recall}\nТочность: ${response.precision}\nПравильность: ${response.accuracy}\nОшибка: ${response.error}\nF-мера ${response.fMeasure}`))
                }
            },
            text: "Метрики"
        });

        const helpButton = ViewUtils.tag({
            name: "button",
            attributes: {
                class: "btn-default"
            },
            eventListeners: {
                click: () => {
                    alert("Введите запрос и нажмите клавишу Enter, чтобы выполнить поиск по документам.\nНажмите кнопку 'Метрики', чтобы просмотреть значения метрик релевантности запросов."); 
                }
            },
            text: "Помощь"
        });

        this._page = ViewUtils.tag({
            name: "div",
            attributes: {
                class: "page main-page"
            },
            children: [
                ViewUtils.tag({
                    name: "div",
                    child: searchBar
                }),
                ViewUtils.tag({
                    name: "div",
                    attributes: {
                        class: "buttons-container"
                    },
                    children: [helpButton, metricsButton]
                })
            ]
        });
    }
}