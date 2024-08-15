除非建立新檔，才產出完整檔案內容。若需要修改既有的檔案，我已為每行代碼提供行號。請使用行號作為參考，但在其他情況下忽略它們。

因為我很有可能自行手動修改程式內容，我也會隨時更新 Project 內上傳的檔案，請完全依據上傳檔案的行號進行修改，不要參考之前對話中已經修改後的結果。

請以以下 JSON 格式提供您建議的代碼更改：

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

**JSON 格式說明：**

* **更改數組：** 回應應該是一個 JSON 物件，其中每個元素代表對代碼的單個更改。
* **更改對象：** 每個更改對象必須具有以下屬性：
  * **type：** 表示更改類型的字符串。它可以是以下之一：
    * `"remove"`：刪除代碼行。
    * `"insertAfter"`：在特定行之後插入代碼。
    * `"replace"`：用新代碼替換代碼行。
  * **lines：** 指定受更改影響的行號的字符串。
    * 對於 `"remove"` 和 `"replace"`，可以是單個行號（例如 `"15"`）或一系列行（例如 `"10-20"`）。
    * 對於 `"insertAfter"`，這應該是應在其後插入新代碼的行號。
  * **text：** 包含要插入或用作替換的代碼的字符串。對於 `"remove"` 更改，這應該是一個空字符串（`""`）。
  * **first_original_line：** 僅為被修改的原始代碼的第一行。這用於在進行更改之前驗證原始文本。
    * 對於 `"remove"`，這是要刪除的文本的第一行。
    * 對於 `"insertAfter"`，這是將在插入行上方的行。
    * 對於 `"replace"`，這是要替換的文本的第一行。
* **注意逸出字元：** 每個字串必須仔細考慮必要的逸出字元，比如 " 必須使用 \" 等。

**防止偏差一行錯誤的重要事項：**

1. **上下文意識：** 確保 JSON 中提供的 `first_original_line` 與要刪除、在其後插入或替換的代碼的第一行完全匹配。這一行對於準確定位更改位置至關重要。
2. **行號計算：** 驗證 `lines` 字段中指定的行號是否正確，並與原始代碼中的實際行相對應。
3. **應用前審核：** 在應用更改之前，請審核 JSON 輸出以確認行號和 `first_original_line` 值符合您的預期。這將有助於在引入任何偏差一行錯誤之前捕獲它們。

**防止替換錯誤之重要事項：**

1. **一次一個更改：** 如果您提供多個更改，請確保每個更改都獨立且不依賴於先前更改的結果。這樣可以避免錯誤地應用多個更改。
2. **修改項目依行號排序：** 如果您提供多個更改，請按行號順序對它們進行排序，以確保它們按順序應用。
3. **同一個檔案的異動必須合併在同一個 JSON：** 如果有多個 JSON 需要套用在同一個目標檔案，將為替換過程帶來混亂。
4. **每段 JSON 都要建立各別程式碼區塊：** 必須使用程式碼區塊包住每個 JSON，以便容易按一鍵複製取得內容。

**示例：**

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

**優點：**

* **結構化數據：** 這種 JSON 格式提供了一種清晰且結構化的方式來表示代碼更改，使得使用 `process-changes` 端點以編程方式解析和應用它們變得更容易。
* **減少歧義：** 特定格式減少了歧義，並確保 AI 助手的指令被正確解釋。
* **提高效率：** 通過以這種格式提供指令，您可以簡化應用代碼更改的過程，避免需要手動解釋或重寫。
* **驗證：** 包含原始文本允許在進行更改之前進行驗證，減少意外修改的風險。

如果您理解我的指示和上下文，請用一句話回應表示。