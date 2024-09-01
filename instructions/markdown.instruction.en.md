If you need to create a new file or make extensive changes, please provide the complete file content without following the format requirements below.

If you need to modify an existing file, you must strictly follow the format provided below. I have provided line numbers for each line of code. Please use the line numbers as a reference, but ignore them in other cases.

Because I may manually modify the program content myself, I will also update the files uploaded to the Project at any time. Please make modifications entirely based on the line numbers of the uploaded files, without referring to the results of previous modifications in the conversation.

Provide your suggested program changes in the following Markdown format:

<antArtifact identifier="markdown-diff" type="text/markdown" language="markdown" title="Changes">

# FILE_NAME_1 FILE_NAME_1_FIRST_LINE_TIMESTAMP

**Remove**
* From: `FIRST_LINE_TO_BE_REMOVED`
* To: `LAST_LINE_TO_BE_REMOVED`

**InsertBetween**
* From: `FIRST_LINE_BEFORE_INSERTING`
* To: `LAST_LINE_AFTER_INSERTING`
````FILE_NAME_1_MARKDOWN_EXTENSION
MULTILINE_TEXT_TO_INSERT
````

**Replace**
* From: `FIRST_LINE_TO_BE_REPLACED`
* To: `LAST_LINE_TO_BE_REPLACED`
````FILE_NAME_1_MARKDOWN_EXTENSION
MULTILINE_TEXT_TO_REPLACE
````
</antArtifact>

## Important points to prevent replacement errors

1. **File modification date and time**: I will include the file modification date and time on the first line of the document with line numbers. Please append this date and time after the output change file name.
2. **Must include specified delimiter items**: The Markdown document must include the specified XML at the beginning and end, and multi-line code blocks must use four ` characters.
3. **One change at a time**: If you provide multiple changes, make sure each change is independent and does not depend on the results of previous changes. This prevents errors when applying multiple changes.
4. **Original code must include line numbers**: The original code provided in From/To must include line numbers to ensure the replacement location is not incorrect.
5. **Sort modification items by line number**: If you provide multiple changes, please sort them by line number to ensure they are applied in order.
6. **Merge nearby changes**: Please carefully consider merging multiple nearby changes into one continuous change item, while separating changes that are further apart.
7. **Minimum change range**: Please carefully consider including only the minimum necessary change range, meaning that the first and last lines of the change are necessary changes, without including additional lines with no changes.

## Example

<antArtifact identifier="markdown-diff" type="text/markdown" language="markdown" title="Changes">

# file1.css 2024-08-14 08:20:42

**InsertBetween**
* From: `13. h1 {`
* To: `14. }`
````css
  color: var(--primary-color);
  font-size: 1.5rem;
````

**Remove**
* From: `26.   display: flex;`
* To: `26.   display: flex;`

# file2.js 2024-08-15 18:04:05

**Replace**
* From: `12.     function old_function() {`
* To: `14.     return value;`
````js
    function new_function() {
      var result = 'New function'

      return result;
````
</antArtifact>

If you understand my instructions, please respond with one sentence to indicate so.
