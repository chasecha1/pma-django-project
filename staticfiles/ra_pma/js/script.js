// Log to confirm script is being loaded
console.log("Script is loaded and running.");

const header = document.querySelector(".calendar h3");
const dates = document.querySelector(".dates");
const navs = document.querySelectorAll("#prev, #next");

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

let date = new Date();
let month = date.getMonth();
let year = date.getFullYear();

// Function to fetch events for a specific month
function fetchEventsForMonth(year, month) {
  const formattedMonth = (month + 1).toString().padStart(2, '0');  // Month is 0-indexed
  fetch(`/events/get_calendar_events/${year}-${formattedMonth}/`)  // Updated with /events/ prefix
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to fetch events.");
      }
      return response.json();
    })
    .then(events => {
      events.forEach(event => {
        const eventDateElement = document.querySelector(`[data-date="${event.date}"]`);
        if (eventDateElement) {
          // Highlight the event day
          eventDateElement.classList.add('event-day');
          // Store event details for later retrieval when clicking the date
          eventDateElement.dataset.eventDetails = JSON.stringify(event);
        }
      });
    })
    .catch(error => console.error('Error fetching events:', error));
}

// Function to add an event to the calendar
function addEventToCalendar(eventDate, eventTitle, eventDescription) {
  const eventDateElement = document.querySelector(`[data-date="${eventDate}"]`);
  if (eventDateElement) {
    eventDateElement.classList.add('event-day');
    eventDateElement.setAttribute('title', `${eventTitle}: ${eventDescription}`);
    eventDateElement.dataset.eventDetails = JSON.stringify({ title: eventTitle, description: eventDescription });
  } else {
    console.error(`No date element found for ${eventDate}`);
  }
}

// Function to render the calendar
function renderCalendar() {
  console.log(`Rendering calendar for ${months[month]} ${year}`);

  const start = new Date(year, month, 1).getDay();
  const endDate = new Date(year, month + 1, 0).getDate();
  const end = new Date(year, month, endDate).getDay();
  const endDatePrev = new Date(year, month, 0).getDate();

  let datesHtml = "";

  for (let i = start; i > 0; i--) {
    datesHtml += `<li class="inactive">${endDatePrev - i + 1}</li>`;
  }

  for (let i = 1; i <= endDate; i++) {
    let className =
      i === date.getDate() &&
      month === new Date().getMonth() &&
      year === new Date().getFullYear()
        ? ' class="today"'
        : "";
    datesHtml += `<li${className} data-date="${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}" onclick="showEventDetails('${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}')">${i}</li>`;
  }

  for (let i = end; i < 6; i++) {
    datesHtml += `<li class="inactive">${i - end + 1}</li>`;
  }

  dates.innerHTML = datesHtml;
  header.textContent = `${months[month]} ${year}`;

  console.log("Calendar has been rendered.");
  fetchEventsForMonth(year, month);  // Fetch events after rendering the calendar
}

// Event listener for navigation (prev and next buttons)
navs.forEach((nav) => {
  nav.addEventListener("click", (e) => {
    const btnId = e.target.id;
    console.log(`Navigation button clicked: ${btnId}`);

    if (btnId === "prev" && month === 0) {
      year--;
      month = 11;
    } else if (btnId === "next" && month === 11) {
      year++;
      month = 0;
    } else {
      month = btnId === "next" ? month + 1 : month - 1;
    }

    date = new Date(year, month, new Date().getDate());
    year = date.getFullYear();
    month = date.getMonth();

    console.log(`Navigated to: ${months[month]} ${year}`);
    renderCalendar();
  });
});

// Function to show event details when a date is clicked
function showEventDetails(eventDate) {
  const eventDateElement = document.querySelector(`[data-date="${eventDate}"]`);
  if (eventDateElement && eventDateElement.dataset.eventDetails) {
    const eventDetails = JSON.parse(eventDateElement.dataset.eventDetails);
    const modalBody = document.getElementById('eventDetailsBody');
    modalBody.innerHTML = `<strong>${eventDetails.title}</strong><p>${eventDetails.description}</p>`;

    // Show the modal with event details
    const eventDetailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'));
    eventDetailsModal.show();
  } else {
    console.log(`No event found for ${eventDate}`);
    alert('No events for this day.');
  }
}

// Function to add the event to the calendar after submission
addEventForm.addEventListener('submit', function(event) {
  event.preventDefault();  // Prevent default form submission

  const eventTitle = document.getElementById('eventTitle').value;
  const eventDate = document.getElementById('eventDate').value;
  const eventDescription = document.getElementById('eventDescription').value;

  const eventData = { title: eventTitle, date: eventDate, description: eventDescription };

  fetch('/events/add_event/', {  // Updated with /events/ prefix
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(eventData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to add event.');
    }
    return response.json();
  })
  .then(data => {
    if (data.status === 'success') {
      alert('Event added successfully!');
      addEventToCalendar(eventDate, eventTitle, eventDescription);  // Add the event immediately to the calendar
      addEventForm.reset();
      const modal = bootstrap.Modal.getInstance(document.getElementById('addEventModal'));
      modal.hide();
    } else {
      alert('Error adding event: ' + data.message);
    }
  })
  .catch(error => console.error('Error:', error));
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Initially render the calendar
renderCalendar();
