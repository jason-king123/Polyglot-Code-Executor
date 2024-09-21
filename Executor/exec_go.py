import subprocess
import resource
import json
import tempfile
import os
import psutil
import time
import threading

class GoExecutor:
    def __init__(self, tmp_dir='tmp'):
        self.tmp_dir = tmp_dir
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

    def compile_go(self, code, tmpdirname):
        filename = os.path.join(tmpdirname, 'main.go')
        executable = os.path.join(tmpdirname, 'main')

        with open(filename, 'w') as file:
            file.write(code)
        subprocess.run(['go', 'build', '-o', executable, filename], check=True)

        return executable

    def monitor_memory(self, child_process, result):
        max_memory = 0
        while child_process.is_running():
            try:
                current_memory = child_process.memory_info().rss
                max_memory = max(max_memory, current_memory)
            except psutil.NoSuchProcess:
                break
            time.sleep(0.05)
        result['max_memory'] = max_memory

    def measure_runtime_and_memory(self, executable, test_data, timeout=5):
        start_time = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime

        process = subprocess.Popen([executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        child_pid = process.pid
        child_process = psutil.Process(child_pid)

        result = {}

        monitor_thread = threading.Thread(target=self.monitor_memory, args=(child_process, result))
        monitor_thread.start()

        stdout, _ = process.communicate(input=test_data, timeout=timeout)
        monitor_thread.join()

        end_time = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime

        max_memory = result.get('max_memory', 0)
        runtime = (end_time - start_time) * 1000  # ms
        runmemory = max_memory / 1024  # KB

        return runtime, runmemory, stdout

    def code_test(self, code, tests, answers):
        if len(tests) != len(answers):
            return json.dumps({
                "exec_outcome": "the number of test cases is not equal to the number of answers",
                "wrong_cases": 0,
                "runtime": 0,
                "runmemory": 0,
                "outputs" : []
            }, indent=4)

        with tempfile.TemporaryDirectory(dir=self.tmp_dir) as tmpdirname:
            try:
                executable = self.compile_go(code, tmpdirname)
                wrong_cases = 0
                runtimes = 0
                memories = 0
                outputs = []

                for test_data, answer in zip(tests, answers):
                    try:
                        runtime, runmemory, stdout = self.measure_runtime_and_memory(executable, test_data)

                        actual_result = stdout.strip()
                        outputs.append(actual_result)
                        if answer.strip() != actual_result.strip():
                            wrong_cases += 1

                        runtimes += runtime
                        memories += runmemory
                    except subprocess.TimeoutExpired:
                        return json.dumps({
                            "exec_outcome": "Timeout",
                            "wrong_cases": wrong_cases,
                            "runtime": runtimes,
                            "runmemory": memories,
                            "outputs" : outputs
                        }, indent=4)
                    except Exception as e:
                        return json.dumps({
                            "exec_outcome": "Runtime Error",
                            "error_message": str(e),
                            "wrong_cases": wrong_cases,
                            "runtime": runtimes,
                            "runmemory": memories,
                            "outputs" : outputs
                        }, indent=4)

                result = {
                    "exec_outcome": "Success" if wrong_cases == 0 else "Failure",
                    "wrong_cases": wrong_cases,
                    "runtime": runtimes,
                    "runmemory": memories,
                    "outputs" : outputs
                }

            except subprocess.CalledProcessError as e:
                return json.dumps({
                    "exec_outcome": "Compilation Error",
                    "error_message": e.output.decode() if e.output else str(e),
                }, indent=4)
            except Exception as e:
                return json.dumps({
                    "exec_outcome": "Error",
                    "error_message": str(e),
                }, indent=4)
            return json.dumps(result, indent=4)