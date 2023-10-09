class ViewDocumentPage extends Page {
    buildPage(documentText) {
        const backButton = ViewUtils.tag({
            name: "button",
            attributes: {
                class: "btn-default"
            },
            eventListeners: {
                click: () => {
                    router.navigate(searchResultsPage);
                }
            },
            text: "Назад"
        });

        const docTextContainer = ViewUtils.tag({
            name: "p",
            text: documentText
        });

        this._page = ViewUtils.tag({
            name: "div",
            attributes: {
                class: "page view-document-page"
            },
            children: [
                docTextContainer,
                ViewUtils.tag({
                    name: "div",
                    attributes: {
                        class: "buttons-container"
                    },
                    child: backButton
                })
            ]
        })
    }
}