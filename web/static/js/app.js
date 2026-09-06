document.addEventListener('DOMContentLoaded', () => {
    
    const elements = {
        authCount: document.getElementById('auth-count'),
        blockCount: document.getElementById('block-count'),
        allowlistBody: document.getElementById('allowlist-body'),
        blocklistBody: document.getElementById('blocklist-body'),
        activeBody: document.getElementById('active-body'),
        logContainer: document.getElementById('log-container'),
        monitorStatus: document.getElementById('monitor-status'),
        pulse: document.querySelector('.pulse')
    };

    // Update stats and tables
    async function updatePolicyData() {
        try {
            const [policyRes, statsRes, activeRes] = await Promise.all([
                fetch('/api/policy'),
                fetch('/api/stats'),
                fetch('/api/active')
            ]);
            
            const policy = await policyRes.json();
            const stats = await statsRes.json();
            const active = await activeRes.json();

            // Update stats
            elements.authCount.textContent = stats.authorized_count;
            elements.blockCount.textContent = stats.blocked_count;
            
            // Update Allowlist Table
            elements.allowlistBody.innerHTML = '';
            if(policy.authorized_devices && policy.authorized_devices.length > 0) {
                policy.authorized_devices.forEach(dev => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${dev.description || 'Unknown'}</strong></td>
                        <td><span style="font-family:monospace; color:var(--text-secondary)">${dev.vendor_id}:${dev.product_id}</span></td>
                        <td>${dev.serial_number || 'N/A'}</td>
                        <td><span class="badge allowed">Allowed</span></td>
                    `;
                    elements.allowlistBody.appendChild(tr);
                });
            } else {
                elements.allowlistBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--text-secondary)">No devices authorized.</td></tr>';
            }

            // Update Blocklist Table
            elements.blocklistBody.innerHTML = '';
            if(policy.blocked_devices && policy.blocked_devices.length > 0) {
                policy.blocked_devices.forEach(dev => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${dev.description || 'Unknown'}</strong></td>
                        <td><span style="font-family:monospace; color:var(--text-secondary)">${dev.vendor_id}:${dev.product_id}</span></td>
                    `;
                    elements.blocklistBody.appendChild(tr);
                });
            } else {
                elements.blocklistBody.innerHTML = '<tr><td colspan="2" style="text-align:center; color:var(--text-secondary)">No devices explicitly blocked.</td></tr>';
            }

            // Update Active Devices Table
            elements.activeBody.innerHTML = '';
            if(active && active.length > 0) {
                active.forEach(dev => {
                    const tr = document.createElement('tr');
                    const drives = dev.drive_letters ? dev.drive_letters.join(', ') : 'None';
                    tr.innerHTML = `
                        <td><strong>${dev.caption || 'Unknown'}</strong></td>
                        <td><span style="font-family:monospace; color:var(--text-secondary)">${dev.vendor_id}:${dev.product_id}</span></td>
                        <td>${dev.serial_number || 'N/A'}</td>
                        <td><span class="badge allowed">${drives}</span></td>
                    `;
                    elements.activeBody.appendChild(tr);
                });
            } else {
                elements.activeBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--text-secondary)">No USB devices currently connected. (Make sure monitor is running)</td></tr>';
            }
            
        } catch (error) {
            console.error('Error fetching policy data:', error);
            elements.monitorStatus.textContent = 'Connection Error';
            elements.monitorStatus.style.color = 'var(--accent-red)';
            elements.pulse.style.backgroundColor = 'var(--accent-red)';
            elements.pulse.style.boxShadow = 'none';
        }
    }

    // Update Logs
    let lastLogContent = '';
    async function updateLogs() {
        try {
            const res = await fetch('/api/logs');
            const data = await res.json();
            
            const currentLogContent = data.logs.join('\n');
            if (currentLogContent !== lastLogContent) {
                elements.logContainer.innerHTML = '';
                data.logs.forEach(line => {
                    const div = document.createElement('div');
                    div.className = 'log-line';
                    
                    // Simple syntax highlighting based on text
                    let formattedLine = line;
                    if(line.includes(' INFO ')) {
                        formattedLine = line.replace(' INFO ', ' <span class="log-info">INFO</span> ');
                    } else if(line.includes(' WARNING ') || line.includes(' ALERT ')) {
                        formattedLine = line.replace(/ (WARNING|ALERT) /, ' <span class="log-warn">$1</span> ');
                    } else if(line.includes(' ERROR ')) {
                        formattedLine = line.replace(' ERROR ', ' <span class="log-error">ERROR</span> ');
                    }
                    
                    // Highlight BLOCKLISTED / AUTHORIZED
                    formattedLine = formattedLine.replace('[BLOCKLISTED]', '<span class="log-error">[BLOCKLISTED]</span>');
                    formattedLine = formattedLine.replace('[UNAUTHORIZED]', '<span class="log-error">[UNAUTHORIZED]</span>');
                    formattedLine = formattedLine.replace('[AUTHORIZED]', '<span class="log-info">[AUTHORIZED]</span>');
                    formattedLine = formattedLine.replace('[SPOOF ALERT]', '<span class="log-warn">[SPOOF ALERT]</span>');

                    div.innerHTML = formattedLine;
                    elements.logContainer.appendChild(div);
                });
                
                // Auto-scroll to bottom
                elements.logContainer.scrollTop = elements.logContainer.scrollHeight;
                lastLogContent = currentLogContent;
            }
        } catch (error) {
            console.error('Error fetching logs:', error);
        }
    }

    // Initial load
    updatePolicyData();
    updateLogs();

    // Poll every 3 seconds
    setInterval(() => {
        updatePolicyData();
        updateLogs();
    }, 3000);
});
