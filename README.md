# LLMCoderSync

Work with [ClaudeSync](https://github.com/jahwag/ClaudeSync) and [LLMCoder](https://github.com/ChrisTorng/LLMCoder) for easy Claude project coding experience.

![](images/LLMCoderServer.png)
The WebUI shows all files, you choose which files to be synced with or without line number. Then press "Sync All" button to sync to target Claude project, with the help from [ClaudeSync](https://github.com/jahwag/ClaudeSync).

You can modify your `SyncCommand` file for your sync tools, not limited to `LLMCoderSync` and `ClaudeSync`.

You can easily choose the current working files to sync, save more tokens from Claude usage for longer conversations.

The line number options is used for [LLMCoder](https://github.com/ChrisTorng/LLMCoder), it uses code with line numbers and ask LLM to use specific JSON diff output, then apply the JSON diff to the source code. It helps you sync the output of LLM back to your source code with only one paste action, and save the output tokens for only diff part.

# Installation

```
pip install flask
```

# Build

```
pip install pyinstaller
pyinstaller LLMCoderSync.spec
pyinstaller LLMCoderServer.spec
```

Run `/path/to/LLMCoderSync/dist/LLMCoderServer/LLMCoderServer` from your project dir `current`, open http://localhost:5000 for WebUI.

Run `/path/to/LLMCoderSync/dist/LLMCoderSync` to copy `current` dir into another `current.sync` dir, for all files synced, with specific line numberred files to sync to LLM (I'm using Claude).

# Usage

Claude custom instruction sample:

```
Please provide concise and brief answers unless detailed explanations are requested.
For any response involving modifications to existing code, strictly follow the instructions in instruction.en.md.
All code should be obtained directly from the uploaded files in the Project, without referencing recent modification results.
```

Run `python LLMCoderServer.py` then open `http://localhost:5000/` in browser.

Run `LLMCoderSync` every time after codes are modified. You can add `claudesync project sync` after it, makes the command be `LLMCoderSync&claudesync project sync`.