// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

/// <reference types="cypress"/>

export {};
import { authorization } from './authorization';
import { forms } from './forms';

declare global {
    namespace Cypress {
        interface Chainable {
            formRequest(url: string, formData: string): Chainable;
            preserveCookies(): Chainable;
            loginAdmin(path: string): Chainable;
        }
    }
}

Cypress.Commands.add("formRequest", (url: string, formData: string) => {
    return cy
        .intercept("POST", url)
        .as("formRequest")
        .window()
        .then(window => {
            var xhr = new window.XMLHttpRequest();
            xhr.open('POST', url);
            xhr.withCredentials = true;
            xhr.send(formData);
        })
        .wait('@formRequest');
});

Cypress.Commands.add("preserveCookies", () => {
    Cypress.Cookies.preserveOnce(
        "sessionid"
    );
});

Cypress.Commands.add("loginAdmin", (path: string) => {
    authorization.fillInlogInData(Cypress.env("TEST_USER_LOGIN"), Cypress.env("TEST_USER_PASSWORD"));
    forms.submit('LoadPage');

    cy.visit(path)
});