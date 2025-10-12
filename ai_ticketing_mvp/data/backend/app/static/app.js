document.addEventListener('DOMContentLoaded', () => {
    const ticketForm = document.getElementById('ticket-form');
    const ticketList = document.getElementById('ticket-list');

    // Function to fetch and display all tickets
    const fetchTickets = async () => {
        try {
            const response = await fetch('/api/tickets/');
            if (!response.ok) throw new Error('Failed to fetch tickets');
            const tickets = await response.json();

            ticketList.innerHTML = ''; // Clear current list
            if (tickets.length === 0) {
                ticketList.innerHTML = '<p>No tickets found.</p>';
                return;
            }

            tickets.reverse().forEach(ticket => {
                const ticketElement = document.createElement('div');
                ticketElement.className = 'ticket';
                ticketElement.innerHTML = `
                    <h3>${ticket.summary}</h3>
                    <p>${ticket.description}</p>
                    <div class="ticket-meta">
                        <span>ID: ${ticket.ticket_id}</span> | 
                        <span>Status: ${ticket.status}</span> |
                        <span>Created: ${new Date(ticket.created_at).toLocaleString()}</span>
                    </div>
                    <p><strong>AI-Predicted Category:</strong> <span class="ticket-category">${ticket.category}</span></p>
                `;
                ticketList.appendChild(ticketElement);
            });
        } catch (error) {
            ticketList.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    };

    // Function to handle form submission
    ticketForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const summary = document.getElementById('summary').value;
        const description = document.getElementById('description').value;

        try {
            const response = await fetch('/api/tickets/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ summary, description })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create ticket');
            }

            ticketForm.reset(); // Clear the form
            fetchTickets(); // Refresh the ticket list
        } catch (error) {
            alert(`Error creating ticket: ${error.message}`);
        }
    });

    // Initial fetch of tickets when the page loads
    fetchTickets();
});