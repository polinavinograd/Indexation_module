class HttpClient {
    _serverAddress;

    constructor(serverAddress) {
        this._serverAddress = serverAddress;
    }

    get(params) {
        return this._request(params, "GET");
    }

    post(params) {
        return this._request(params, "POST");
    }

    put(params) {
        return this._request(params, "PUT");
    }

    delete(params) {
        return this._request(params, "DELETE", false);
    }

    async _request(params, method, jsonifyResponse = true) {
        let requestAddress = `${this._serverAddress}/${params.path}`;
        if (params.queryParams !== undefined) {
            requestAddress += `?${params.queryParams.toString()}`;
        }

        const headers = params.headers ?? new Headers();
        headers.append("Content-Type", "application/json");

        return fetch(requestAddress, {
            method,
            headers,
            body: params.body !== undefined ? JSON.stringify(params.body) : undefined
        })
            .then(response => jsonifyResponse ? response.json() : response);
    }
}
