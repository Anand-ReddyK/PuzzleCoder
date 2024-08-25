import redis
import json
import subprocess
import os
r = redis.Redis(host='redis', port=6379, db=0)

def execute_code(language, user_code, testcases):

    try:
        if language == "python":
            file_extension = 'py'
            execute_command = ["python", "user_code.py"]

        elif language == "java":
            file_extension = 'java'
            execute_command = ["java", "Main"]
        
        elif language == "javascript":
            file_extension = 'js'
            execute_command = ["node", "user_code.js"]
        
        code_filename = f"user_code.{file_extension}"
        with open(code_filename, "w") as code_file:
            code_file.write(user_code)
        
        results_info = {}
        results_info["results"] = []
        total_testcases = len(testcases)
        passed_testcases = 0
        for testcase in testcases:
            input = testcase["input"]
            expected_output = testcase["expected_output"]

            if language == "java":
                complie_code = subprocess.run(['javac', 'user_code.java'], text=True, capture_output=True)
                if complie_code.returncode != 0:
                    os.remove(code_filename)
                    return complie_code.stderr
            
            result = subprocess.run(execute_command, input=input, text=True, capture_output=True)

            actual_output = result.stdout.strip()
            passed = expected_output.lower() == actual_output.lower()
            results_info["results"].append({
                "input": input,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "passed": passed
            })

            if passed:
                passed_testcases += 1
        
        pass_rate = (passed_testcases / total_testcases)
        results_info["pass_rate"] = pass_rate
        
        os.remove(code_filename)
        if language == "java":
            os.remove("Main.class")
        
        return results_info
    
    except Exception as e:
        return str(e)


while True:
    _, message = r.blpop("code_queue")
    task = json.loads(message)
    result = execute_code(task["language"], task["code"], task["test_cases"])
    result["problem_id"] = task["problem_id"]
    print(result, f"code_result_{task['user_id']}")
    r.set(f'code_result_{task["user_id"]}', json.dumps(result))
