const apiUrl = `${Cypress.env("apiUrl")}`

describe('Backend Test Spec', () => {

  // TODO: 'Cannot GET with a request body'

  let account_id = '566944be-2dab-460b-b3ed-eeeebd8c5618'

  it('should call ping', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/ping`,
    }).then((response) => {
      expect(response.status).to.eq(200)
      expect(response.body).to.eq("pong")
    })
  })

  it('unknown transaction should fail with 404', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/transaction/566944be-2dab-460b-b3ed-eeee00000000`,
    }).then((response) => {
      expect(response.status).to.eq(404)
    })
  })

  it('unknown account should fail with 404', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/accounts/566944be-2dab-460b-b3ed-eeee00000000`,
    }).then((response) => {
      expect(response.status).to.eq(404)
    })
  })

  it('Improperly formatted transaction id should fail with 400', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/transaction/justbad`,
    }).then((response) => {
      expect(response.status).to.eq(400)
    })
  })

  it('Impropertly formatted account id should fail with 400', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/accounts/sobad!`,
    }).then((response) => {
      expect(response.status).to.eq(400)
    })
  })

  it('create a transaction with 0 amount should fail', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'POST',
      body: {"account_id": "566944be-2dab-460b-b3ed-eeeebd8c5618", "amount": 0},
      url: `${apiUrl}/transaction`,
    }).then((response) => {
      expect(response.status).to.eq(400)
    })
  })

  it('create a transaction with non-zero amount should pass', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'POST',
      body: {"account_id": "566944be-2dab-460b-b3ed-eeeebd8c5618", "amount": 100},
      url: `${apiUrl}/transaction`,
    }).then((response) => {
      expect(response.status).to.eq(201)
    })
  })

  it('Cannot create a transaction with no request body', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'POST',
      url: `${apiUrl}/transaction`,
    }).then((response) => {
      expect(response.status).to.eq(400)
    })
  })

  it('Can GET an account', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/accounts/${account_id}`,
    }).then((response) => {
      expect(response.status).to.eq(200)
      expect(response.body.account_id).to.eq(account_id)
    })
  })

  it('Transaction yields correct balance and is properly recorded', () => {
    cy.request({
      failOnStatusCode: false,
      method: 'GET',
      url: `${apiUrl}/accounts/${account_id}`,
    }).then((response) => {
      let balanceBefore = response.body.balance
      let transactionAmount = 10
      cy.request({
        failOnStatusCode: false,
        method: 'POST',
        body: { "account_id": account_id, "amount": transactionAmount },
        url: `${apiUrl}/transaction`,
      }).then((response) => {
        expect(response.status).to.eq(201)
        let transaction_id = response.body.transaction_id
        cy.request({
          failOnStatusCode: false,
          method: 'GET',
          url: `${apiUrl}/transaction/${transaction_id}`,
        }).then((response) => {
          expect(response.status).to.eq(200)
          expect(response.body.account_id).to.eq(account_id)
          expect(response.body.transaction_id).to.eq(transaction_id)
          expect(response.body.amount).to.eq(transactionAmount)
        })

        cy.request({
          failOnStatusCode: false,
          method: 'GET',
          url: `${apiUrl}/accounts/${account_id}`,
        }).then((response) => {
          expect(response.status).to.eq(200)
          expect(response.body.account_id).to.eq(account_id)
          expect(response.body.balance).to.eq(balanceBefore + transactionAmount)
        })    
      })
    })
  })
})
