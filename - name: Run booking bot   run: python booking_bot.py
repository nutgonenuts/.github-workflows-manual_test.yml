name: Parkalot Booking Bot

on:
  workflow_dispatch:

jobs:
  booking:
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout repository
      - name: Checkout repository
        uses: actions/checkout@v3

      # Step 2: Set up Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install selenium webdriver-manager

      # Step 4: Run booking bot
      - name: Run booking bot
        env:
          PARKALOT_EMAIL: ${{ secrets.PARKALOT_EMAIL }}
          PARKALOT_PASSWORD: ${{ secrets.PARKALOT_PASSWORD }}
        run: python booking_bot.py
