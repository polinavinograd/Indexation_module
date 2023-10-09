class Page {
    _page;

    constructor() {
        this.buildPage();
    }

    get htmlElem() { return this._page; }
}