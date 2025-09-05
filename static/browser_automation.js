/**
 * Client-side browser automation
 * This script runs in the user's browser to help with form filling
 */

class InvescoFormHelper {
    constructor(extractedData) {
        this.data = extractedData;
        this.formUrl = 'https://www.invesco-ug.com/business/application/new';
        this.loginUrl = 'https://www.invesco-ug.com/auth/login';
    }

    /**
     * Open the Invesco form in a new tab with instructions
     */
    openForm() {
        // Create a new window with the form
        const formWindow = window.open(this.formUrl, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
        
        if (formWindow) {
            // Wait for the window to load, then inject helper script
            formWindow.addEventListener('load', () => {
                this.injectHelperScript(formWindow);
            });
            
            // Also show instructions in current window
            this.showInstructions();
        } else {
            alert('Please allow popups for this site to open the form automatically.');
            // Fallback: just open the URL
            window.open(this.formUrl, '_blank');
        }
    }

    /**
     * Show detailed instructions for manual form filling
     */
    showInstructions() {
        const instructions = this.generateInstructions();
        const modal = this.createModal('Form Filling Instructions', instructions);
        document.body.appendChild(modal);
    }

    /**
     * Generate step-by-step instructions
     */
    generateInstructions() {
        const certType = this.data.Certificate_Type || 'Normal';
        const border = this.data.Out_Bound_Border || 'UNKNOWN';
        
        return `
            <div class="form-instructions">
                <h4>📋 Step-by-Step Instructions:</h4>
                <ol>
                    <li><strong>Login:</strong> If not already logged in, go to the login page and enter your credentials</li>
                    <li><strong>Navigate to Form:</strong> Go to the new application form</li>
                    <li><strong>Fill Dropdowns:</strong>
                        <ul>
                            <li><strong>Issuing Body:</strong> Select "DR CONGO"</li>
                            <li><strong>Cert. Type:</strong> Select "${certType === 'AD' ? 'CONTINUANCE' : 'REGIONAL'}"</li>
                            <li><strong>Cargo Origin:</strong> Select "${certType === 'AD' ? 'OUTSIDE UGANDA' : 'UGANDA'}"</li>
                            <li><strong>Shipment Route:</strong> Select "OUT-BOUND"</li>
                            <li><strong>Transport Mode:</strong> Select "ROAD"</li>
                            <li><strong>FOB Currency:</strong> Select "USD"</li>
                            <li><strong>Freight Currency:</strong> Select "USD"</li>
                            <li><strong>Out-Bound Border:</strong> Select "${border}"</li>
                        </ul>
                    </li>
                    <li><strong>Fill Text Fields:</strong> Copy the values from the table below</li>
                    <li><strong>Submit:</strong> Review and submit the form</li>
                </ol>
                
                <h4>📊 Data to Copy:</h4>
                <div class="data-copy-section">
                    ${this.generateDataCopySection()}
                </div>
                
                <div class="button-group">
                    <button onclick="copyAllData()" class="btn btn-primary">📋 Copy All Data</button>
                    <button onclick="copyField('certificateNumber', '${this.data.Certificate_No || ''}')" class="btn btn-secondary">Copy Certificate No</button>
                    <button onclick="copyField('importerName', '${this.data.Importer || ''}')" class="btn btn-secondary">Copy Importer</button>
                    <button onclick="copyField('exporterName', '${this.data.Exporter || ''}')" class="btn btn-secondary">Copy Exporter</button>
                </div>
            </div>
        `;
    }

    /**
     * Generate data copy section
     */
    generateDataCopySection() {
        const fields = [
            { key: 'Certificate_No', label: 'Certificate Number', value: this.data.Certificate_No || '' },
            { key: 'Entry_No', label: 'Entry Number', value: this.data.Entry_No || '' },
            { key: 'Importer', label: 'Importer', value: this.data.Importer || '' },
            { key: 'Exporter', label: 'Exporter', value: this.data.Exporter || '' },
            { key: 'Forwarder', label: 'Forwarder', value: this.data.Forwarder || '' },
            { key: 'transporterName', label: 'Transporter', value: this.data.transporterName || 'OWN' },
            { key: 'Transport', label: 'Vehicle Number', value: this.data.Transport || '' },
            { key: 'Discharge_Place', label: 'Discharge Location', value: this.data.Discharge_Place || '' },
            { key: 'Final_Destination', label: 'Final Destination', value: this.data.Final_Destination || '' },
            { key: 'FOB_Value', label: 'FOB Value', value: this.data.FOB_Value || '' },
            { key: 'Base_Freight', label: 'Freight Value', value: this.data.Base_Freight || '' },
            { key: 'validationNotes', label: 'Validation Notes', value: this.data.validationNotes || 'please verify' },
            { key: 'Descriptions', label: 'Cargo Description', value: Array.isArray(this.data.Descriptions) ? this.data.Descriptions.join('\\n') : (this.data.Descriptions || '') }
        ];

        return fields.map(field => `
            <div class="data-field">
                <label><strong>${field.label}:</strong></label>
                <div class="field-value">
                    <input type="text" value="${field.value}" readonly class="form-control" id="field-${field.key}">
                    <button onclick="copyField('${field.key}', '${field.value.replace(/'/g, "\\'")}')" class="btn btn-sm btn-outline-primary">Copy</button>
                </div>
            </div>
        `).join('');
    }

    /**
     * Create a modal dialog
     */
    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal fade show';
        modal.style.display = 'block';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" onclick="this.closest('.modal').remove()"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" onclick="this.closest('.modal').remove()">Close</button>
                        <button type="button" class="btn btn-primary" onclick="openInvescoForm()">Open Invesco Form</button>
                    </div>
                </div>
            </div>
        `;
        return modal;
    }

    /**
     * Inject helper script into the form window
     */
    injectHelperScript(formWindow) {
        try {
            const script = `
                // Helper functions for the form window
                function highlightField(selector) {
                    const element = document.querySelector(selector);
                    if (element) {
                        element.style.border = '2px solid #007bff';
                        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => {
                            element.style.border = '';
                        }, 3000);
                    }
                }
                
                // Highlight important fields
                setTimeout(() => {
                    highlightField('input[id="certificateNumber"]');
                    highlightField('input[id="importerName"]');
                    highlightField('input[id="exporterName"]');
                }, 2000);
            `;
            
            formWindow.eval(script);
        } catch (e) {
            console.log('Could not inject helper script (cross-origin restrictions)');
        }
    }
}

// Global functions for the HTML buttons
function openInvescoForm() {
    const extractedData = window.extractedData || {};
    const helper = new InvescoFormHelper(extractedData);
    helper.openForm();
}

function copyAllData() {
    const extractedData = window.extractedData || {};
    const dataStr = JSON.stringify(extractedData, null, 2);
    
    navigator.clipboard.writeText(dataStr).then(() => {
        alert('All data copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        // Fallback
        const textArea = document.createElement('textarea');
        textArea.value = dataStr;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        alert('All data copied to clipboard!');
    });
}

function copyField(fieldKey, value) {
    navigator.clipboard.writeText(value).then(() => {
        // Visual feedback
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('btn-success');
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('btn-success');
        }, 1000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Make extracted data available globally
    if (typeof window.extractedData === 'undefined') {
        window.extractedData = {};
    }
});
