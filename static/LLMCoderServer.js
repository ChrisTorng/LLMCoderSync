document.addEventListener('DOMContentLoaded', function() {
    const syncCheckboxes = document.querySelectorAll('.sync-checkbox');

    syncCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const filePath = this.closest('tr').querySelector('td:last-child').textContent;
            const shouldSync = this.checked;

            fetch('/update_sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file: filePath,
                    should_sync: shouldSync
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log(`Sync status updated for ${filePath}`);
                } else {
                    console.error(`Failed to update sync status for ${filePath}`);
                    // Revert the checkbox state if the update failed
                    this.checked = !shouldSync;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert the checkbox state if there was an error
                this.checked = !shouldSync;
            });
        });
    });
});