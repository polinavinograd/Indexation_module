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
            },
            eventListeners: {
                keyup: (event) => {
                    if (event.key !== 'Enter') {
                        return;
                    }
                    // httpClient.post({
                    //     path: "docs",
                    //     body: {
                    //         query: event.target.value
                    //     }
                    // });
                    Promise.resolve(docArrayMock)
                        .then(response => {
                            searchResultsPage.buildPage(response);
                            router.navigate(searchResultsPage);
                        });
                }
            }
        });

        const metricsButton = ViewUtils.tag({
            name: "button",
            eventListeners: {
                click: () => {
                    // httpClient.get({
                    //     path: "metrics"
                    // })
                    Promise.resolve({
                        recall: 1,
                        precision: 0.8,
                        accuracy: 0.6,
                        error: 0.4,
                        fMeasure: 0.2
                    })
                        .then(response => alert(`
                            Полнота: ${response.recall}
                            Точность: ${response.precision}
                            Правильность: ${response.accuracy}
                            Ошибка: ${response.error}
                            F-мера ${response.fMeasure}
                        `))
                }
            },
            text: "Метрики"
        });

        const helpButton = ViewUtils.tag({
            name: "button",
            eventListeners: {
                click: () => { alert("help!"); }
            },
            text: "Помощь"
        });

        this._page = ViewUtils.tag({
            name: "div",
            children: [
                ViewUtils.tag({
                    name: "div",
                    child: searchBar
                }),
                ViewUtils.tag({
                    name: "div",
                    children: [metricsButton, helpButton]
                })
            ]
        });
    }
}