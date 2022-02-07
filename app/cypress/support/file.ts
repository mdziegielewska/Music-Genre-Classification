/// <reference types="cypress"/>

import 'cypress-file-upload';

class Files {
    uploadFile(filePath: string) {
        cy.get('input[type="file"]').attachFile(filePath);
        cy.get('[name="submit"]]').click();
    }
}

export const file = new Files()