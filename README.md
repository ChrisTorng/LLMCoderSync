# LLMCoderSync
Work with ClaudeSync and LLMCoder for easy Claude coding experience.

# Build

```
pip install pyinstaller
pyinstaller --onefile LLMCoderSync.py
```

Run with `./dist/LLMCoderSync` or `python LLMCoderSync.py`.

# Usage

Claude custom instruction sample:

```
使用繁體中文台灣用語回答。程式內容請完全以英文撰寫，包括顯示訊息及註解。請精簡扼要回答，除非要求詳細說明。每次的回覆若有牽涉到修改現有程式碼，必須完全依 instruction.zh-tw.md 中的指示來進行。
```

Run `LLMCoderSync` every time after codes are modified.