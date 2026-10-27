# Lab 5: Static Code Analysis — Issue Table and Reflection

**Student:** Ruthik  
**SRN:** PES1UG25CS837  
**Program:** `energy_system.py` — Energy Consumption & Tariff Calculator

## Issue table

| Issue | Tool/category | Original location | Change made |
|---|---|---|---|
| Mutable default argument `history=[]` retained shared state between calls | Pylint / correctness | Original line 12 | Changed default to `None` and creates a fresh list when omitted. |
| `eval(adjustment)` allowed arbitrary Python expressions to execute | Bandit / security | Original line 63 | Replaced `eval` with integer parsing and validation. |
| Bare `except:` hid every possible failure while loading JSON | Pylint / reliability | Original line 44 | Catches specific file, encoding, and JSON errors; reports invalid data. |
| Files were opened without a context manager and the save path did not guarantee closure on error | Pylint / resource handling | Original lines 42–49 | Used `Path.read_text` and `Path.write_text` with UTF-8. |
| Negative unit readings were accepted | Input validation | Original line 55 example | Rejects negative readings and requires integer units. |
| Unused `sys` import | Pylint / maintainability | Original line 2 | Removed the unused import. |
| Program ran immediately on import | Maintainability / testability | Original line 68 | Added `if __name__ == "__main__":` guard. |

**Note:** The table describes changes in the supplied corrected script. The actual report line numbers and tool findings must be confirmed by rerunning the tools on the original and corrected files. Do not claim a Pylint score or clean report until the commands show it.

## Reflection answers

1. **What is static code analysis?**  
   Static code analysis examines source code without running it to identify potential bugs, security weaknesses, and style issues.

2. **What does Pylint do?**  
   Pylint checks Python code quality, naming, structure, unused imports, and potential mistakes.

3. **What does Bandit do?**  
   Bandit scans Python code for common security risks, such as unsafe use of `eval`.

4. **What does Flake8 do?**  
   Flake8 checks Python formatting and style, including many PEP 8 rules.

5. **Why run the tools before and after fixing code?**  
   The first run records the original findings. The second run checks whether the changes removed them and whether any problems remain.

6. **What did you learn?**  
   Static analysis helps find risky or hard-to-maintain code early. Fixing unsafe evaluation, overly broad exception handling, shared mutable defaults, and file handling improves safety and reliability.
