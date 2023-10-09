class ViewDocumentPage extends Page {
    buildPage(documentText) {
        const backButton = ViewUtils.tag({
            name: "button",
            eventListeners: {
                click: () => {
                    router.navigate(searchResultsPage);
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

        const docTextContainer = ViewUtils.tag({
            name: "p",
            text: documentText
        });

        this._page = ViewUtils.tag({
            name: "div",
            children: [
                docTextContainer,
                ViewUtils.tag({
                    name: "div",
                    children: [backButton, helpButton]
                })
            ]
        })
    }
}