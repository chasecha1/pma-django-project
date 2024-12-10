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
    const formattedMonth = (month + 1).toString().padStart(2, '0');
    const url = `/events/get_calendar_events/${year}-${formattedMonth}/`;

    fetch(url)
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
                    eventDateElement.classList.add('event-day');
                    eventDateElement.dataset.eventDetails = JSON.stringify(event);
                }
            });
        })
        .catch(error => console.error('Error fetching events:', error));
}

function addJoinedEventToCalendar(eventDate, eventTitle, eventDescription) {
    const eventDateElement = document.querySelector(`[data-date="${eventDate}"]`);
    if (eventDateElement) {
        eventDateElement.classList.add('event-day');
        eventDateElement.setAttribute('title', `${eventTitle}: ${eventDescription}`);
        eventDateElement.dataset.eventDetails = JSON.stringify({
            title: eventTitle,
            description: eventDescription
        });
    } else {
        console.error(`No date element found for ${eventDate}`);
    }
}


// Function to add event to the calendar dynamically
function addEventToCalendar(eventDate, eventTitle, eventDescription) {
  const eventDateElement = document.querySelector(`[data-date="${eventDate}"]`);
  if (eventDateElement) {
    eventDateElement.classList.add('event-day');
    eventDateElement.setAttribute('title', `${eventTitle}: ${eventDescription}`);
    eventDateElement.dataset.eventDetails = JSON.stringify({
      title: eventTitle,
      description: eventDescription
    });
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

    const eventDetailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'));
    eventDetailsModal.show();
  } else {
    console.log(`No event found for ${eventDate}`);
    alert('No events for this day.');
  }
}

// Function to add the event to the calendar after submission
const addEventForm = document.getElementById('addEventForm');

if (addEventForm) {
  addEventForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const eventData = {
      title: document.getElementById('eventTitle').value,
      date: document.getElementById('eventDate').value,
      description: document.getElementById('eventDescription').value,
    };

    const addEventUrl = '/events/add_event/';
    const addEventModal = document.getElementById('addEventModal');
    const modalInstance = bootstrap.Modal.getInstance(addEventModal);

    fetch(addEventUrl, {
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
        // Properly hide the modal
        if (modalInstance) {
          modalInstance.hide();
        }

        // Remove modal backdrop manually if it persists
        const modalBackdrop = document.querySelector('.modal-backdrop');
        if (modalBackdrop) {
          modalBackdrop.remove();
        }

        // Reset body styles
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';

        // Reset the form
        addEventForm.reset();

        // Add the event to the calendar dynamically
        addEventToCalendar(eventData.date, eventData.title, eventData.description);

        // Optionally re-render the calendar
        renderCalendar();

        window.location.reload();

        // Show success message
        alert('Event added successfully!');
      } else {
        alert('Error adding event: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while adding the event. Please try again.');

      // Ensure modal is closed even on error
      if (modalInstance) {
        modalInstance.hide();
      }
      const modalBackdrop = document.querySelector('.modal-backdrop');
      if (modalBackdrop) {
        modalBackdrop.remove();
      }
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    });
  });
} else {
  console.error("addEventForm element not found.");
}

// Add event listener for modal hidden event
const addEventModal = document.getElementById('addEventModal');
if (addEventModal) {
  addEventModal.addEventListener('hidden.bs.modal', function () {
    // Clean up any remaining modal artifacts
    const modalBackdrop = document.querySelector('.modal-backdrop');
    if (modalBackdrop) {
      modalBackdrop.remove();
    }
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
  });
}

// Function to fetch CSRF token from cookies
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