/// <reference types="cypress"/>

class Results {
    verifyResult(genre: string) {
        cy.log('verifying result');

        cy.get('[name="genre"]')
            .should('contain', genre);
    }
}

export const results = new Results();