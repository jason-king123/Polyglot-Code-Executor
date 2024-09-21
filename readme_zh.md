# Polyglot Code Executor 多语言代码执行器

**其他语言版本: [English](readme.md)**

## 简介

欢迎使用 Polyglot Code Executor，一款多功能且强大的工具，能够执行多种流行编程语言的代码。对于需要简单、易部署且稳定、准确的代码执行环境的开发者来说，这是一个理想的解决方案。

**欢迎在 GitHub 上为这个项目点赞支持，参与讨论，贡献代码或提出改进建议！**

## 功能特性

- **多语言支持**：支持13种不同的编程语言执行代码，包括C++、C、C#、Go、Java、JavaScript、PHP、Python、Ruby、Kotlin、Swift、Rust 和 R。
- **简便部署**：支持本地和 Docker 两种简单的部署方式。
- **性能指标**：提供代码执行时间和内存使用的详细反馈。
- **结果校验**：通过与预期结果的对比，确保代码的正确性。

## 待解决的问题

我们正在积极解决以下问题，以提升 Polyglot Code Executor 的功能：

- **C# (csc)**：没有找到文件或目录：'csc'。
- **Java**：Java 程序没有输出。
- **Kotlin**：命令 '['kotlinc', 'tmp/tmprx55xua7/Main.kt', '-include-runtime', '-d', 'tmp/tmprx55xua7']' 返回非零退出状态 2。
- **Swift**：没有找到文件或目录：'swiftc'。
- **Rust**：没有找到文件或目录：'rustc'。

## 未来改进

我们将不断改进 Polyglot Code Executor，以下是我们计划在未来版本中推出的一些增强功能：

- **新增语言支持**：我们计划根据社区需求增加更多的编程语言支持。
- **扩展性能指标**：我们将提供更详细的性能数据，帮助用户优化代码。
- **用户界面**：可能会开发基于 Web 的用户界面，方便用户与执行器交互。
- **自定义选项**：允许用户自定义执行环境，以更好地满足特定需求。
- **社区贡献**：我们欢迎开源社区的贡献，帮助扩展执行器的功能。

## 部署

您有两种部署 Polyglot Code Executor 的方式：

1. **本地部署**：在项目根目录下执行以下命令：
   ```bash
   python app.py
   ```
   这将在本地 `localhost` 的 `9999` 端口启动应用。

2. **Docker 部署**：使用以下命令通过 Docker 构建并运行应用：
   ```bash
   docker build -t code_exec:13 .
   docker run --cpus="5" -p 9999:9999 --name my_code_exec code_exec:13
   ```

## 使用说明

要执行代码，使用 `code_exec` 函数，传入代码、测试用例和预期结果。以下是一个示例用法：

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

# 示例用法
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

### 参数说明

- `code`：要执行的源代码。
- `tests`：测试用例列表，每个用例为一个字符串。
- `answers`：与测试用例相对应的预期结果列表。
- `lang`：指定编程语言的代码（如 `cpp`, `python`, `java`, `c`, `csharp`, `go`, `js`, `php`, `ruby`, `kotlin`, `swift`, `rust`, `r`）。

### 示例输出

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

## 贡献指南

我们非常欢迎对 Polyglot Code Executor 的贡献。如果您有改进建议、新增语言的需求或发现了需要修复的 bug，请随时提交 pull request 或在 GitHub 仓库中创建 issue。

---

感谢您选择 Polyglot Code Executor 作为您的多语言代码执行环境。我们致力于为开发者提供一个稳定且用户友好的开发工具。