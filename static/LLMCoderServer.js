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
    syncAllButton.addEventListener('click', function() {
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
                console.log('Sync completed for all files');
                alert('Sync completed for all files');
            } else {
                console.error('Failed to sync all files');
                alert('Failed to sync all files');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during sync');
        });
    });
});