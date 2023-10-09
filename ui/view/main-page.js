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
                    // httpClient.get({
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
                click: () => { alert("metrics!"); }
            },
            text: "Расчёт метрик"
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