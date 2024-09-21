# Polyglot Code Executor

**Read this in other languages: [中文](readme_zh.md).**

## Introduction
Welcome to the Polyglot Code Executor, a versatile and powerful tool designed to execute code in a multitude of popular programming languages. This project is the perfect solution for developers who need a simple, easy-to-deploy environment that offers stability and accuracy in code execution.

**Star this project on GitHub to show your support, and don't hesitate to join the discussion, contribute, or suggest improvements!**

## Features

- **Multi-Language Support**: Execute code in 13 different programming languages including C++, C, C#, Go, Java, JavaScript, PHP, Python, Ruby, Kotlin, Swift, Rust, and R.
- **Easy Deployment**: Simple deployment process with both local and Docker options.
- **Performance Metrics**: Receive detailed feedback on the execution time and memory usage of your code.
- **Accuracy**: Ensures the correctness of your code by comparing it against expected results.

## Existing Problems to be Solved

We are actively addressing the following issues to improve the Polyglot Code Executor:

- **C# (csc)**: No such file or directory: 'csc'.
- **Java**: Java programs are not producing output.
- **Kotlin**: Command '['kotlinc', 'tmp/tmprx55xua7/Main.kt', '-include-runtime', '-d', 'tmp/tmprx55xua7']' returned non-zero exit status 2..
- **Swift**: No such file or directory: 'swiftc'.
- **Rust**: No such file or directory: 'rustc'.

## Future Enhancements

We are continuously working to improve the Polyglot Code Executor. Here are some of the enhancements and features we are planning for future releases:

- **Additional Language Support**: We plan to add support for more programming languages based on community demand.
- **Extended Performance Metrics**: We aim to provide more detailed performance data to help users optimize their code.
- **User Interface**: A web-based user interface may be developed for easier interaction with the executor.
- **Customization Options**: Allow users to customize the execution environment to better fit their specific needs.
- **Community Contributions**: We welcome contributions from the open-source community to expand the capabilities of the executor.

## Deployment

You have two options to deploy the Polyglot Code Executor:

1. **Local Deployment**: Run the application locally by executing the following command in the project root directory:
   ```bash
   python app.py
   ```
   This will deploy the application to `localhost` on port `9999`.

2. **Docker Deployment**: Build and run the application using Docker with the following commands:
   ```bash
   docker build -t code_exec:13 .
   docker run --cpus="5" -p 9999:9999 --name my_code_exec code_exec:13
   ```

## Usage

To execute code, use the `code_exec` function by passing the code, test cases, and expected answers. Here's a sample usage:

```python
import json
import requests

def code_exec(code, tests, answers, lang):
    data = {
        'code': code,
        'tests': tests,
        'answers': answers
    }
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    url = f'http://localhost:9999/{lang}'
    response = requests.post(url, data=payload, headers=headers)
    response_data = json.loads(response.text)
    return response_data['result']

# Example usage
code = """
#include <iostream>
int main() {
    int num1, num2, sum;
    std::cin >> num1 >> num2;
    sum = num1 + num2;
    std::cout << sum;
    return 0;
}
"""
result = code_exec(code, ['10 5'], ['15'], 'cpp')
print(result)
```

### Parameters

- `code`: The source code to be executed.
- `tests`: A list of test cases as strings.
- `answers`: A list of expected results corresponding to the test cases.
- `lang`: The language code (`cpp`, `python`, `java`, `c`, `csharp`, `go`, `js`, `php`, `ruby`, `kotlin`, `swift`, `rust`, `r`) to specify the programming language.

### Response Example

```json
{
    "exec_outcome": "Success",
    "wrong_cases": 0,
    "runtime": 7.880999999999361,
    "runmemory": 1828.0,
    "outputs": [
        "15"
    ]
}
```

## Contributing

We welcome contributions to the Polyglot Code Executor. If you have an idea for improvement, a new language to add, or a bug to fix, please submit a pull request or create an issue in our GitHub repository.

---

Thank you for choosing the Polyglot Code Executor for your multi-language coding needs. We are committed to providing a robust and user-friendly environment for developers.
