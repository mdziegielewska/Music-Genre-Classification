/// <reference types="cypress"/>

import { authorization } from '../support/authorization'
import { forms } from '../support/forms'

describe('Log in', () => {
    beforeEach(() => {
        cy.visit('/sign-in');
    })

    it('Should log in correctly', () => {
        authorization.fillInlogInData(Cypress.env("TEST_USER_LOGIN"), Cypress.env("TEST_USER_PASSWORD"));
        forms.submit('LoadPage');

        cy.url()
            .should('contain', '/');
    })

    it('Should log in incorrectly', () => {
        authorization.fillInlogInData(Cypress.env("TEST_USER_LOGIN"), "TESTESTEST123");
        forms.submit('LoadPage');

        authorization.failedLoginAlertShouldContain('Invalid password');

        cy.url()
            .should('contain', '/sign-in');
    })

    it('Should log in incorrectly 3 times', () => {
        for(var i=0; i<2; i++) {
            authorization.fillInlogInData(Cypress.env("TEST_USER_LOGIN"), "TESTESTEST123");
            forms.submit('LoadPage');

            if (i == 1) {
                authorization.failedLoginAlertShouldContain('Do you want to reset your password?');
            } else {
                authorization.failedLoginAlertShouldContain('Invalid password');
            }
        }

        cy.url()
            .should('contain', '/sign-in');
    })
})