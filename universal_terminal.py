from dotenv import load_dotenv

load_dotenv()

import platform
import os
import subprocess
from openai import OpenAI
from pydantic import BaseModel
import instructor

class Command(BaseModel):
    correctCommand: str
    description: str

client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

def get_os_info():
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()

    try:
        processor = platform.processor()
    except Exception:
        processor = "Unknown"

    if system == "Darwin":
        os_name = f"macOS {platform.mac_ver()[0]}"
    elif system == "Windows":
        os_name = f"Windows {release}"
    elif system == "Linux":
        try:
            os_name = subprocess.check_output(["lsb_release", "-ds"]).decode().strip()
        except:
            try:
                with open("/etc/os-release") as f:
                    os_release = dict(line.strip().split("=") for line in f if "=" in line)
                os_name = os_release.get("PRETTY_NAME", "Linux")
            except:
                os_name = "Linux"
    else:
        os_name = system

    return {
        "OS Name": os_name,
        "OS Release": release,
        "OS Version": version,
        "Machine": machine,
        "Processor": processor
    }

def get_shell_info():
    if platform.system() == "Windows":
        return os.environ.get("COMSPEC", "cmd.exe")
    else:
        return os.environ.get("SHELL", "/bin/sh")

def run_command(command, shell):
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(f'{shell} /c {command}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        else:
            process = subprocess.Popen([shell, '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            return f"Command Output:\n{stdout.strip()}"
        else:
            if "command not found" in stderr.lower() or "is not recognized as an internal or external command" in stderr.lower():
                try:
                    extracted_data = client.chat.completions.create(
                        model="gpt-4",
                        response_model=Command,
                        messages=[
                            {"role": "system", "content": f'''You are a terminal expert.
                                You are given a command and the error message.
                                You need to extract the correct command that can run on the following shell:
                                <Shell Info>
                                    {shell}
                                </Shell Info>
                                The command is the correct command that can run on the shell.
                                The description is an optional field, in case no command is available as an alternative for the given shell. In this case, return echo "No alternative found".'''},
                            {"role": "user", "content": f"Command: {command}\nError: {stderr.strip()}"}
                        ]
                    )
                    if platform.system() == "Windows":
                        process = subprocess.Popen(f'{shell} /c {extracted_data.correctCommand}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
                    else:
                        process = subprocess.Popen([shell, '-c', extracted_data.correctCommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                    output = stdout.strip() if stdout else stderr.strip()
                    return f'''Command Not Found
{'=' * 20}
Incorrect Command: {command}
Suggested Command: {extracted_data.correctCommand}

LLM Description:
{extracted_data.description}

Command Output:
{output}
{'=' * 20}'''
                except Exception as e:
                    return f"Error: {e}"
            return f"Error:\n{stderr.strip()}"
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except FileNotFoundError:
        return "Command not available, use something else"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    os_info = get_os_info()
    shell = get_shell_info()

    print("Operating System Information:")
    for key, value in os_info.items():
        print(f"  {key}: {value}")

    print(f"\nDefault Shell: {shell}")

    while True:
        command = input("\nEnter a command (or 'exit' to quit): ").strip()
        if command.lower() == 'exit':
            break
        
        result = run_command(command, shell)
        print("\nResult:")
        print(result)

if __name__ == "__main__":
    main()