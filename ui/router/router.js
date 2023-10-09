class Router {
    _outletRef;

    constructor(outletElemId) {
        this._outletRef = document.getElementById(outletElemId);
    }

    navigate(page) {
        this._outletRef.innerHTML = "";
        this._outletRef.appendChild(page.htmlElem);
    }
}