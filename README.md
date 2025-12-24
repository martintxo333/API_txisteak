# API bidezko txiste programa [EUS]

API bidez txisteak jasotzen, itzultzen eta terminalean kolorez erakusten dituen Python programa.
Txisteak fitxategi batean gordetzen dira UTF-8 kodifikazioarekin.

---

# Joke API Translator Program [EN]

## Project Description

This project is a **learning exercise** developed for the subject **Industrial Informatics** at the **University of the Basque Country (EHU)**.

The program was **independently conceived and developed** as a personal initiative with the goal of practicing **Python programming** while working with **external APIs**, error handling, terminal formatting, and file management.

The application uses **two APIs**:

* **JokeAPI** to retrieve jokes in **English** and **Spanish**
* **Google Translate** to automatically translate English jokes into **Basque (Euskera)**

Jokes are displayed in the terminal using **different colors** depending on the language, API **response times are measured**, and all results are stored in a text file using **UTF-8 encoding** to properly handle special characters.

This project is intended for **educational purposes**.

---

## Technologies Used

* **Python 3**
* **requests** – for API requests
* **colorama** – for colored terminal output (ANSI colors)
* **JokeAPI** – joke retrieval
* **Google Translate API** -- for translation to Basque
* **Visual Studio Code** – recommended development environment

---

## Features

* Gets jokes in **English** and **Spanish**
* Automatically translates the English joke into **Basque**
* Displays jokes using **colored terminal output**
* Measures API response times
* Handles API connection errors (`try/except`)
* Prevents repetition of Spanish jokes
* Saves all jokes to a UTF-8 encoded file (`txisteak.txt`)
* Interactive command-line menu

---

## Requirements

* Python 3.x
* Internet connection
* Required Python libraries:

  ```bash
  pip install requests colorama
  ```

---

## Usage

```bash
python API_txisteak_kontatu_itzuli.py
```

Follow the terminal instructions to choose how many jokes you want to display.

---

## Author

**Martin Maiz Negredo**

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for license rights and limitations.
