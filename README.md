# Cross-Platform CLI Tool

This Python script provides a powerful cross-platform command-line interface (CLI) tool that allows users to execute commands across different operating systems. It's particularly useful for developers and system administrators who work with multiple OS environments.

## Features

- Executes commands in the default shell of the current OS
- Provides intelligent command suggestions when a command is not found
- Offers explanations for command differences across platforms
- Handles Windows, macOS, and Linux environments

## Setup

1. Clone this repository or download the script.
2. Install the required dependencies:
   ```
   pip install python-dotenv openai pydantic instructor
   ```
3. Create a `.env` file in the same directory as the script and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the script using Python:

```
python universal_terminal.py
```

The tool will display information about your current operating system and prompt you to enter commands.

### Example Usage

```
Operating System Information:
  OS Name: macOS 12.3
  OS Release: 21.4.0
  OS Version: Darwin Kernel Version 21.4.0
  Machine: x86_64
  Processor: i386

Default Shell: /bin/zsh

Enter a command (or 'exit' to quit): dir

Result:
Command Not Found
====================
Incorrect Command: dir
Suggested Command: ls

LLM Description:
The 'dir' command is used in Windows to list directory contents. On macOS and Linux, the equivalent command is 'ls'.

Command Output:
[List of files and directories]
====================

Enter a command (or 'exit' to quit): exit
```

## Benefits

- **Cross-Platform Compatibility**: Execute commands seamlessly across different operating systems.
- **Learning Tool**: Understand command differences between OS environments.
- **Intelligent Suggestions**: Get alternative command suggestions when a command is not available on the current OS.
- **Detailed OS Information**: Quickly retrieve system details for troubleshooting or documentation.

This tool is invaluable for developers working in multi-OS environments, system administrators managing diverse systems, or anyone looking to enhance their command-line skills across different platforms.
