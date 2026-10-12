document.querySelectorAll("[data-doctor]").forEach((link) => {
    link.addEventListener("click", () => {
        const doctorSelect = document.getElementById("doctor_id");
        doctorSelect.value = link.dataset.doctor;
    });
});

const appointmentDate = document.querySelector('input[name="appointment_date"]');
if (appointmentDate) {
    const today = new Date();
    const localToday = [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0")
    ].join("-");
    appointmentDate.min = localToday;
}
