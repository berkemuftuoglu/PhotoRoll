# PhotoRoll

![PhotoRoll Logo](app/static/images/photoroll_logo.png)

## Introduction
PhotoRoll is a versatile web application dedicated to creating, storing, and sending invoices efficiently and effectively.

## Technology
- Backend: Flask
- Frontend: HTML/CSS/JS
- Styling: Bulma CSS [https://bulma.io/]
- Database: SQLite3 with SQLalchemy [https://www.sqlalchemy.org/] 

## Prerequisites
To get started with PhotoRoll, ensure you have the following installed:
- Anaconda or Miniconda
- All required packages listed in `environment.yml`

## Setup with Conda
Follow these steps to set up PhotoRoll using Conda:

```bash
git clone https://github.com/berkemuftuoglu/PhotoRoll.git
cd PhotoRoll
conda env create -f environment.yml
conda activate photoroll
flask run
```

## Setting up Emailing Service
PhotoRoll's `send_email_with_attachment()` function is tailored for use with the Gmail SMTP server. To utilize this service with Gmail:

1. Provide your email address and an app-specific password. (Generate an app password following [Google's guide](https://support.google.com/accounts/answer/185833?hl=en)).
2. Be aware that this setup bypasses 2-factor authentication (2FA), so use it cautiously.

This function is invoked in the `sendinvoice()` function within the `routes.py` file.

## Populating the Data
The included `dum.py` script allows for easy database creation and data generation. Feel free to adjust its parameters to suit your needs.

## Disclaimer
Generative AI has been employed in the development of this project.

## Contributions
For information on how to contribute to PhotoRoll, please refer to the `CONTRIBUTING` file.


