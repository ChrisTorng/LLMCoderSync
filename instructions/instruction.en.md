Only create a complete file content when creating a new file. If you need to modify an existing file, I have provided line numbers for each line of code. Please use the line numbers as references but ignore them otherwise.

Because I am likely to manually modify the program content myself, I will also update the files uploaded to the Project at any time. Please make modifications entirely based on the line numbers of the uploaded files, and do not refer to the results of modifications from previous conversations.

Please provide your suggested code changes in the following JSON format:

```json
[
  {
    "type": "remove",
    "lines": "LINE_NUMBERS",
    "text": "",
    "first_original_line": "FIRST_LINE_OF_ORIGINAL_TEXT_TO_BE_REMOVED"
  },
  {
    "type": "insertAfter",
    "lines": "LINE_NUMBER",
    "text": "CODE_TO_INSERT",
    "first_original_line": "ORIGINAL_TEXT_AFTER_WHICH_CODE_SHOULD_BE_INSERTED"
  },
  {
    "type": "replace",
    "lines": "LINE_NUMBERS",
    "text": "REPLACEMENT_CODE",
    "first_original_line": "FIRST_LINE_OF_ORIGINAL_TEXT_TO_BE_REPLACED"
  }
]
```

**Explanation of JSON Format:**

* **Array of Changes:** The response should be a JSON array, where each element represents a single change to be made to the code.
* **Change Object:** Each change object must have the following properties:
  * **type:** A string indicating the type of change. It can be one of the following:
    * `"remove"`: To delete lines of code.
    * `"insertAfter"`: To insert code after a specific line.
    * `"replace"`: To replace lines of code with new code.
  * **lines:** A string specifying the line numbers affected by the change.
    * For `"remove"` and `"replace"`, this can be a single line number (e.g., `"15"`) or a range of lines (e.g., `"10-20"`).
    * For `"insertAfter"`, this should be the line number after which the new code should be inserted.
  * **text:** A string containing the code to be inserted or used as a replacement. For `"remove"` changes, this should be an empty string (`""`).
  * **first_original_line:** Just the first line of the original code that is being modified. This is used to verify the original text before making changes.
    * For `"remove"`, this is the first line of the text being removed.
    * For `"insertAfter"`, this is the line that will be above the inserted line.
    * For `"replace"`, this is the first line of the text being replaced.
* **Note on escape characters:** Each string must carefully consider necessary escape characters, such as using \" for " and so on.

**Important Points to Prevent Off-by-One Errors:**

1. **Context Awareness:** Ensure that the `first_original_line` provided in the JSON matches exactly with the first line of the code to be removed, inserted after, or replaced. This line is crucial for accurately locating the position for changes.
2. **Line Number Calculation:** Verify that the line numbers specified in the `lines` field are correct and correspond to the actual lines in the original code.
3. **Review Before Applying:** Before applying the changes, review the JSON output to confirm that the line numbers and the `first_original_line` values match your expectations. This will help catch any off-by-one errors before they are introduced.

**Important Points to Prevent Replacement Errors:**

1. **One Change at a Time:** If you provide multiple changes, ensure that each change is independent and does not rely on the result of previous changes. This prevents errors in applying multiple changes.
2. **Sort Modifications by Line Number:** If you provide multiple changes, sort them by line number to ensure they are applied in order.
3. **Combine Changes for the Same File in One JSON:** If there are multiple JSONs to be applied to the same target file, it will cause confusion in the replacement process.
4. **Create Separate Code Blocks for Each JSON:** Each JSON must be enclosed in a code block to easily copy its content with one click.

**Example:**

```json
[
  {
    "type": "remove",
    "lines": "13",
    "text": "",
    "first_original_line": "    echo 'Line to be removed';"
  },
  {
    "type": "insertAfter",
    "lines": "25",
    "text": "    echo 'Inserted line of code';",
    "first_original_line": "    echo 'Line above inserted code';"
  },
  {
    "type": "replace",
    "lines": "30-32",
    "text": "    function new_function() {\n        return 'New function';\n    }",
    "first_original_line": "    function old_function() {"
  }
]
```

**Benefits:**

* **Structured Data:** This JSON format provides a clear and structured way to represent code changes, making it easier to parse and apply them programmatically using the `process-changes` endpoint.
* **Reduced Ambiguity:** The specific format reduces ambiguity and ensures that the AI assistant's instructions are interpreted correctly.
* **Improved Efficiency:** By providing instructions in this format, you can streamline the process of applying code changes and avoid the need for manual interpretation or rewriting.
* **Verification:** The inclusion of the original text allows for verification before making changes, reducing the risk of unintended modifications.

If you understand my instructions and the context, please indicate it with a one-sentence response.