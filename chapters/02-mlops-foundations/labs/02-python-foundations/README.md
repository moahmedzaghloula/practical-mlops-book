# Lab 02 — Python Foundations

This lab introduces an executable Python program and the control flow that later
training and inference scripts build upon.

## Run the Program

```bash
cd chapters/02-mlops-foundations/labs/02-python-foundations
chmod +x add.py
./add.py
```

It can also be invoked through the interpreter:

```bash
python3 add.py
```

## Validate the Script

```bash
python3 -m py_compile add.py
```

## Concepts Practiced

- shebang-based execution
- executable file permissions
- functions and return values
- loops and generated examples
- the `if __name__ == "__main__"` entry-point pattern

## Production Connection

Small functions are easier to test and reuse in training scripts, batch jobs,
APIs, and workflow orchestrators. Explicit entry points also keep import-time
behavior separate from command-line execution.
