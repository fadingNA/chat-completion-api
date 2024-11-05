# Welcome to Chatminal Contributing Guidelines

Thank you for choosing to contribute to Chatminal!

# We accept different types of contributions

📣 **Discussions** - Engage in conversations, start new topics, or help answer questions.

🐞 **Issues** - This is where we keep track of tasks. It could be bugs, fixes or suggestions for new features.

🛠️ **Pull requests** - Suggest changes to our repository, either by working on existing issues or adding new features.

# Getting started

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/fadingNA/chat-completion-api.git
   cd chat-completion-api
   pip install -r requirements.txt # if you are using pip3 change pip to pip3 instead.

   cd app # to run the play.py file or app/play.py
   ```

## Issue & Pull Request

- **Fork the repository** and clone it locally.
- **Create a branch** for your edits.
- We have only one server using Python 3.7+ and an OpenAI API key.
  Before creating a pull request, please make sure your changes are working properly.

## Code Formatting and Linting

**Formatting using Black:**

```bash
black app/
```

- Black is a Python code formatter that reformats your code to make it more readable. It is recommended to run this command before creating a pull request.

**Linting using Flake8:**

```bash
flake8 app/
```

- Flake8 is a Python code linter that checks your code for stylistic or programming errors. It is recommended to run this command before creating a pull request.

---

**Configuration:**

For the flake8 configuration, we have a `.flake8` file in the root directory of the repository. This file contains the configuration for flake8, such as the maximum line length and the list of ignored errors.

```
[flake8]
max-line-length = 150
ignore = F405 , W293, W291

```

---

**Testing Overview**

To ensure code quality adn functionality, we have a few tests in place. You can run the tests using the following command:

```bash
python3 -m unittest discover -s test
```

To run specific tests, you can use the following command:

```bash
python3 -m unittest test.test_play
```

To run specific test cases, you can use the following command:

```bash
python3 -m unittest test.test_play.TestPlay.test_play
```

---

**🚨 Note:**

- **`format.py` Script:** Ensure that before creating a pull request, you run the `format.py` script to format the code and check for linting errors.

- **Dependencies:** The contributors should have `black` and `flake8` installed in their environment to run `format.py` successfully.

- **Vscode Extension:** You can also use the `Python` extension in Visual Studio Code to format the code using `black` and check for linting errors using `flake8`.

---
