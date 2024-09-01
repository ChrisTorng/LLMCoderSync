# LLMCoderSync

Enhance your coding experience with Claude AI by integrating [ClaudeSync](https://github.com/jahwag/ClaudeSync) and [LLMCoder](https://github.com/ChrisTorng/LLMCoder).

![LLMCoderServer Interface](images/LLMCoderServer.png)

The LLMCoderServer web interface displays all files in your project, excluding those ignored by `.gitignore` and `.claudesync`. You can select which files to sync, with or without line numbers. Click the `Sync All` button to synchronize your selected files to the target Claude project, utilizing [ClaudeSync](https://github.com/jahwag/ClaudeSync).

## Key Features

- Customize your sync process by modifying the `SyncCommand` file to work with your preferred sync tools, not limited to `LLMCoderSync` and `ClaudeSync`.
- Easily select current working files for synchronization, optimizing Claude token usage for longer conversations.
- Line number options designed for [LLMCoder](https://github.com/ChrisTorng/LLMCoder), enabling efficient code updates using specific Markdown diff output.
- Streamlined workflow: Sync LLM output back to your source code with a single paste action, saving output tokens by focusing on diff parts only.

## Build & Usage

1. Install required packages:
   ```
   pip install flask pyinstaller
   ```

2. Build the executables:
   ```
   pyinstaller LLMCoderSync.spec
   pyinstaller LLMCoderServer.spec
   ```

3. From your project directory, run:
   ```
   /path/to/LLMCoderSync/dist/LLMCoderServer/LLMCoderServer
   ```

4. Open http://localhost:5000 to access the web interface.

5. Select the files you want to sync. If you're not using [LLMCoder](https://github.com/ChrisTorng/LLMCoder), uncheck all line numbers.

6. Run the following command to copy your `current` directory to `current.sync`, including all synced files with specified line-numbered files:
   ```
   /path/to/LLMCoderSync/dist/LLMCoderSync
   ```

7. Use `claudesync project select` to choose the `current.sync` directory as your project directory.

8. Click the `Sync All` button in the web interface to execute `SyncCommand` and verify that synchronization is working correctly.

## Integration with [LLMCoder](https://github.com/ChrisTorng/LLMCoder)

The key point of [LLMCoder](https://github.com/ChrisTorng/LLMCoder) is using Markdown diff format for less token usage. It apply the diff to the source code to get the modified result code. You can see the README.md of [LLMCoder](https://github.com/ChrisTorng/LLMCoder) for more detail.


1. Copy `SyncCommand` or `SyncCommand.cmd` (for Windows) into your project directory.

2. Create a `.claudeignore` file with the following content:
   ```
   .*
   LICENSE
   SyncCommand*
   ```

3. In  the web interface, uncheck any files that should not be synced or have line numbers added, then click `Sync All`.

4. Set Claude's Project custom instructions with the content from [instructions/markdown.instruction.en.md](instructions/markdown.instruction.en.md) after your specific instructions.

5. When asking Claude to modify code, it will follow the instructions and output a Markdown diff.

6. On the [LLMCoder online page](https://christorng.github.io/LLMCoder/), paste your source code, then paste the Markdown diff. It will automatically apply the changes to the source and copy to your clipboard.

7. Paste the updated code back into your IDE to overwrite the source.

8. Click the `Sync All` button on the web interface after each code modification to ensure the latest code with line numbers is ready for the next prompt.

## Future Plans

- **Integrate LLMCoder into LLMCoderSync WebUI**

  Select a code file, paste Markdown, and write the result directly into the source, saving more time.

- **Apply multiple file changes at once**

  Enhance LLM to include file names in Markdown diffs for simultaneous modifications across multiple files.

- **Automatic line number error correction**

  Implement intelligent detection and correction of incorrect first/last line numbers in LLM output.

- **Auto Sync**

  Detect file changes and sync automatically.

- **Browser extension**

  Integrate with the Claude.ai website for a more streamlined workflow between IDE and LLMCoderSync.