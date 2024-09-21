from flask import Flask, request, jsonify
import json
import os
from Executor.exec_cpp import CppExecutor
from Executor.exec_C import CExecutor
from Executor.exec_CSharp import CSharpExecutor
from Executor.exec_go import GoExecutor
from Executor.exec_java import JavaExecutor
from Executor.exec_JS import JavaScriptExecutor
from Executor.exec_Kotlin import KotlinExecutor
from Executor.exec_PHP import PHPExecutor
from Executor.exec_R import RExecutor
from Executor.exec_Ruby import RubyExecutor
from Executor.exec_Rust import RustExecutor
from Executor.exec_Swift import SwiftExecutor
from Executor.exec_py import PythonExecutor

app = Flask(__name__)

executors = {
    'cpp': CppExecutor(),
    'c' : CExecutor(),
    'csharp' : CSharpExecutor(),
    'go' : GoExecutor(),
    'java' : JavaExecutor(),
    'js' : JavaScriptExecutor(),
    'php' : PHPExecutor(),
    'python': PythonExecutor(),
    'ruby' : RubyExecutor(),
    'kotlin': KotlinExecutor(),
    'swift': SwiftExecutor(),
    'rust': RustExecutor(),
    'r': RExecutor()
}

@app.route('/<lang>', methods=['POST'])
def run_code(lang):
    data = request.json
    code = data.get('code')
    tests = data.get('tests', [])
    answers = data.get('answers', [])

    if not code:
        return jsonify({"error": "No code provided"}), 400

    executor = executors.get(lang)
    if not executor:
        return jsonify({"error": "Language not supported"}), 400

    result_json = executor.code_test(code, tests, answers)
    return jsonify({"result": result_json})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)