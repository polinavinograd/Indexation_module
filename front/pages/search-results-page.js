class SearchResultsPage extends Page {
    buildPage(docArray = []) {
        const backButton = ViewUtils.tag({
            name: "button",
            attributes: {
                class: "btn-default"
            },
            eventListeners: {
                click: () => {
                    router.navigate(mainPage);
                }
            },
            text: "Назад"
        });

        const helpButton = ViewUtils.tag({
            name: "button",
            attributes: {
                class: "btn-default"
            },
            eventListeners: {
                click: () => {
                    alert(`Нажмите на запись в таблице, чтобы увидеть полный текст документа.`);
                }
            },
            text: "Помощь"
        });

        const searchResultsTable = ViewUtils.tag({
            name: "table",
            attributes: {
                class: "search-results-table"
            },
            children: [
                ViewUtils.tag({
                    name: "tr",
                    children: [
                        "Название документа",
                        "Весовые коэффициенты ключевых слов запроса",
                        "Релевантность запросу",
                        "Дата добавления в базу данных",
                        "Первые <=300 символов"
                    ].map(columnHeader => ViewUtils.tag({ name: "th", text: columnHeader }))
                }),
                ...docArray.map(doc => ViewUtils.tag({
                    name: "tr",
                    children: [
                        ViewUtils.tag({ name: "td", text: doc.name }),
                        ViewUtils.tag({
                            name: "td",
                            children: Object.keys(doc.topWords).map(word => ViewUtils.tag({
                                name: "p",
                                text: `${word}: ${doc.topWords[word]}`
                            }))
                        }),
                        ViewUtils.tag({ name: "td", text: doc.relevance }),
                        ViewUtils.tag({ name: "td", text: doc.date }),
                        ViewUtils.tag({ name: "td", text: doc.snippet })
                    ],
                    eventListeners: {
                        click: () => {
                            httpClient.post({
                                path: "text",
                                body: {
                                    docName: doc.name
                                }
                            })
                                .then(response => {
                                    viewDocumentPage.buildPage(response);
                                    router.navigate(viewDocumentPage);
                                });
                        }
                    }
                })),
            ]
        });

        this._page = ViewUtils.tag({
            name: "div",
            attributes: {
                class: "page search-results-page"
            },
            children: [
                searchResultsTable,
                ViewUtils.tag({
                    name: "div",
                    attributes: {
                        class: "buttons-container"
                    },
                    children: [helpButton, backButton]
                })
            ]
        });
    }
}