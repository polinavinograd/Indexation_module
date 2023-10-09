class SearchResultsPage extends Page {
    buildPage(docArray = []) {
        const backButton = ViewUtils.tag({
            name: "button",
            eventListeners: {
                click: () => {
                    router.navigate(mainPage);
                }
            },
            text: "Назад"
        });

        const helpButton = ViewUtils.tag({
            name: "button",
            eventListeners: {
                click: () => { alert("help!"); }
            },
            text: "Помощь"
        });

        const searchResultsTable = ViewUtils.tag({
            name: "table",
            attributes: {
                class: "search-results-table"
            },
            children: docArray.map(doc => ViewUtils.tag({
                name: "tr",
                children: [
                    ViewUtils.tag({ name: "td", text: doc.name }),
                    ViewUtils.tag({
                        name: "td",
                        child: ViewUtils.tag({
                            name: "ul",
                            children: doc.topWords.map(wordWeightObj => ViewUtils.tag({
                                name: "li",
                                text: `${wordWeightObj.word}: ${wordWeightObj.weightCoef}`
                            }))
                        })
                    }),
                    ViewUtils.tag({ name: "td", text: doc.relevance }),
                    ViewUtils.tag({ name: "td", text: doc.date }),
                    ViewUtils.tag({ name: "td", text: doc.snippet })
                ],
                eventListeners: {
                    click: () => {
                        // httpClient.get({
                        //     path: "text",
                        //     body: {
                        //         docName: doc.name
                        //     }
                        // })
                        Promise.resolve('This is the full text of a document.')
                            .then(response => {
                                viewDocumentPage.buildPage(response);
                                router.navigate(viewDocumentPage);
                            });
                    }
                }
            })),
        });

        this._page = ViewUtils.tag({
            name: "div",
            children: [
                searchResultsTable,
                ViewUtils.tag({
                    name: "div",
                    children: [backButton, helpButton]
                })
            ]
        });
    }
}