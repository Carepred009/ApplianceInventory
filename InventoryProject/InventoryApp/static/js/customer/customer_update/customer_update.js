

 document.getElementById("updateForm").addEventListener("submit", function(event) {
     event.preventDefault(); // prevent auto submit for testing
     if (confirm("Are you sure you want to update this record?")) {
         this.submit(); // submit if confirmed
     }
 });