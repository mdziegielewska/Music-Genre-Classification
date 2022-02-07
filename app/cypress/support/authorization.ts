/// <reference types="cypress"/>

class Authorization {
    fillInlogInData(username: string, password: string) {
        cy.log('filling in user data');

        cy.get('#username')
            .type(username);

        cy.get('#password')
            .type(password);
    }

    failedLoginAlertShouldContain(alert: string) {
        cy.log('verifying failed login alert');

        cy.get('#failed-login-alert')
            .should('be.visible')
            .and('contain', alert);
    }

    logOut() {
        cy.log('logging out');

        cy.get('[name="logout"]')
            .click();
    }
}

export const authorization = new Authorization();