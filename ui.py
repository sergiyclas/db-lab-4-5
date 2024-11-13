import gradio as gr
from my_project.auth.service.user_service import CustomerService, TransactionService, TransactionAccountService, \
    AccountService

customer_service = CustomerService()
account_service = AccountService()
transaction_service = TransactionService()
transaction_account_service = TransactionAccountService()

with gr.Blocks() as demo:
    gr.Markdown("# Manage Customers")
    with gr.Row():
        customer_name = gr.Textbox(label="Customer Name", placeholder="Enter customer name")
        customer_email = gr.Textbox(label="Email", placeholder="Enter email")
        customer_phone = gr.Textbox(label="Phone", placeholder="Enter phone number")
        customer_id = gr.Textbox(label='ID(to POST or DELETE method)', placeholder="Enter id customer(Optional)")
    add_customer_btn = gr.Button("Add Customer")
    change_customer_btn = gr.Button("Update Customer")
    del_customer_btn = gr.Button('Delete Customer')
    customer_output = gr.JSON(label="Output")
    add_customer_btn.click(customer_service.create_customer, inputs=[customer_name, customer_email, customer_phone],
                           outputs=customer_output)
    change_customer_btn.click(customer_service.update_customer,
                              inputs=[customer_id, customer_name, customer_email, customer_phone],
                              outputs=customer_output)
    del_customer_btn.click(customer_service.delete_customer,
                           inputs=[customer_id],
                           outputs=customer_output)

    show_customers_btn = gr.Button("Show All Customers")
    customers_output = gr.DataFrame(headers=["ID", "Name", "Email", "Phone"], label="Customers", interactive=False)
    show_customers_btn.click(
        lambda: [customer.values() for customer in customer_service.get_all_customers()],
        outputs=customers_output
    )

    gr.Markdown("# Manage Accounts")
    with gr.Row():
        customer_id_for_account = gr.Textbox(label="Customer ID", placeholder='Enter Customer id to connect')
        account_number = gr.Textbox(label="Account Number", placeholder="Enter account number")
        account_balance = gr.Textbox(label="Balance", placeholder='Enter balance sum')
        account_id = gr.Textbox(label="ID(to POST or DELETE method)", placeholder='Enter id account(Optional)')

    add_account_btn = gr.Button("Add Account")
    update_account_btn = gr.Button("Update Account")
    delete_account_btn = gr.Button("Delete Account")
    account_output = gr.JSON(label="Output")
    add_account_btn.click(account_service.create_account,
                          inputs=[customer_id_for_account, account_number, account_balance],
                          outputs=account_output)

    update_account_btn.click(account_service.update_account,
                             inputs=[account_id, customer_id_for_account, account_number, account_balance],
                             outputs=account_output)

    delete_account_btn.click(account_service.delete_account,
                             inputs=[account_id],
                             outputs=account_output)

    with gr.Row():
        accounts_customer_id_input = gr.Textbox(label="Customer ID to find all Accounts",
                                                placeholder='Enter customer id')
    show_accounts_btn = gr.Button("Show Accounts for Customer")
    accounts_output = gr.DataFrame(headers=["ID", "Customer ID", "Balance", "Balance"], label="Accounts",
                                   interactive=False)

    show_accounts_btn.click(
        lambda accounts_customer_id_input: [account.values() for account in
                                            account_service.get_accounts_by_customer_id(accounts_customer_id_input)],
        inputs=[accounts_customer_id_input],
        outputs=accounts_output
    )

    gr.Markdown("# Manage Transactions")
    with gr.Row():
        transaction_amount = gr.Textbox(label="Transaction Amount", placeholder='Enter Amount of transaction')
        transaction_date = gr.Textbox(label="Transaction Date (YYYY-MM-DD)", placeholder="Enter date")
    add_transaction_btn = gr.Button("Add Transaction")
    transaction_output = gr.JSON(label="Output")
    add_transaction_btn.click(transaction_service.create_transaction, inputs=[transaction_amount, transaction_date],
                              outputs=transaction_output)

    with gr.Row():
        transactions_account_id_input = gr.Number(label="Account ID for Transactions", precision=0)
    show_transactions_btn = gr.Button("Show Transactions for Account")
    transactions_output = gr.DataFrame(
        headers=["ID", "Amount", "Transaction Date", "Fee Amount", "Fee Date", "Status", "Status Date"],
        label="Transactions", interactive=False)
    show_transactions_btn.click(
        lambda transactions_account_id_input: [transaction.values() for transaction in
                                               transaction_account_service.get_transactions_account_by_id(
                                                   transactions_account_id_input)],
        inputs=[transactions_account_id_input],
        outputs=transactions_output
    )

    with gr.Row():
        accounts_id_input = gr.Textbox(label="Account IDs splitted by coma(,): 1, 2, 3, 4")
    show_account_transactions_btn = gr.Button("Show all transactions these accounts")
    account_transactions_output = gr.JSON(label="Output")
    show_account_transactions_btn.click(
        lambda accounts_id_input: transaction_account_service.get_transactions_account_by_ids(str(accounts_id_input).split(',')),
        inputs=[accounts_id_input],
        outputs=account_transactions_output
    )

# demo.launch(share=True)
demo.launch()