/// <reference types="cypress"/>

class Routes {
    expect(key: string) {
        cy.log('expecting route');

        const [method, pattern] = this.getRoute(key);

        cy.intercept(method, pattern).as(key);
    }

    waitFor(key: string) {
        cy.log('waiting for route');

        cy.wait(`@${key}`)
    }

    private getRoute(key:string) {
        switch (key) {
            case 'LoadPage': return ['GET', '/'];

            default: throw Error(`Unknown route key: ${key}`)
        }
    }

    sendRequest(url: string, method: string, body: string) {
        cy.log('sending request');

        cy.request({
            method: method,
            url: url,
            body: body
        }).then(response => {
            expect(response.status).to.be.eq(200);
        });
    }
}

export const routes = new Routes();