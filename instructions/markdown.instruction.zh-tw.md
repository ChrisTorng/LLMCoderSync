若需建立新檔，或者異動範圍太大，請直接產出完整檔案內容，不依下列格式要求。

若需要修改既有的檔案，則必須嚴格按照底下提供的格式輸出。我已為每行代碼提供行號。請使用行號作為參考，但在其他情況下忽略它們。

因為我很有可能自行手動修改程式內容，我也會隨時更新 Project 內上傳的檔案，請完全依據上傳檔案的行號進行修改，不要參考之前對話中已經修改後的結果。

依以下 Markdown 格式提供您建議的程式更改:

<antArtifact identifier="markdown-diff" type="text/markdown" language="markdown" title="異動內容">

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

## 防止替換錯誤之重要事項

1. **檔案修改日期時間**: 我會在附上行號的文件檔之第一行附上檔案修改日期時間，請在輸出之異動檔名後附加該日期時間。
2. **必須包括指定分隔項目**: Markdown 文件的前後必須包括指定的 XML，多行程式碼區塊必須使用四個 ` 字元。
3. **一次一個更改**: 如果您提供多個異動，請確保每個異動都獨立且不依賴於先前更改的結果，這樣可以避免錯誤地套用多個異動。
4. **原始程式必須附上行號**: From/To 所提供的原始程式必須附上行號，保證替換位置不會錯誤。
5. **修改項目依行號排序**: 如果您提供多個更改，請按行號順序對它們進行排序，以確保它們按順序套用。
6. **合併相近異動**: 請仔細考慮相近的多處異動，合併為一個連續的異動項目，而相距較遠的異動則分離項目。
7. **最小異動範圍**: 請仔細考慮僅包含最小必要之異動範圍，也就是異動的第一行及最後一行都是有必要異動之行，不要額外包含無異動內容之行。

## 範例

<antArtifact identifier="markdown-diff" type="text/markdown" language="markdown" title="異動內容">

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
* To: `15.     }`
````js
    function new_function() {
      var result = 'New function'

      return result;
    }
````
</antArtifact>

如果您理解我的指示，請用一句話回應表示。