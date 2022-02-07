/// <reference types="cypress"/>

import { routes } from "./routes";

class Forms {
    submit(route: string) {
        cy.log('submitting form');

        routes.expect(route);

        cy.get('[name="submit"]')
            .click();

        cy.waitFor(route);
    }

    setUsername(username: string) {
        cy.get('[name="username"]')
            .type(username);
    }
}

export const forms = new Forms();