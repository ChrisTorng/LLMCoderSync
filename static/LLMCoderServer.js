document.addEventListener('DOMContentLoaded', function() {
    const syncCheckboxes = document.querySelectorAll('.sync-checkbox');
    const lineNumberCheckboxes = document.querySelectorAll('.linenumber-checkbox');

    function updateCheckboxState(checkbox, url, fileKey, shouldKey) {
        const filePath = checkbox.closest('tr').querySelector('td:last-child').textContent;
        const shouldValue = checkbox.checked;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                [fileKey]: filePath,
                [shouldKey]: shouldValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log(`${shouldKey} status updated for ${filePath}`);
            } else {
                console.error(`Failed to update ${shouldKey} status for ${filePath}`);
                // Revert the checkbox state if the update failed
                checkbox.checked = !shouldValue;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Revert the checkbox state if there was an error
            checkbox.checked = !shouldValue;
        });
    }

    syncCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateCheckboxState(this, '/update_sync', 'file', 'should_sync');
        });
    });

    lineNumberCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateCheckboxState(this, '/update_line_numbers', 'file', 'should_add_line_numbers');
        });
    });

    const syncAllButton = document.getElementById('syncAllButton');
    const syncOutput = document.getElementById('syncOutput');

    syncAllButton.addEventListener('click', function() {
        syncOutput.textContent = 'Syncing...'; // Show initial message
        fetch('/sync', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'sync_all' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                syncOutput.textContent = data.output;
            } else {
                syncOutput.textContent = 'Failed to sync all files. Error: ' + data.error;
            }
        })
        .catch(error => {
            syncOutput.textContent = 'An error occurred during sync: ' + error;
        });
    });
});