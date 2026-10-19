/* HITS Made Simple — anonymous progress tracking (Google Form).
   Leave formAction empty to switch tracking off.
   Fill these in from the Form's pre-filled link:
   formAction = https://docs.google.com/forms/d/e/<FORM_ID>/formResponse
   fields     = the entry.NNNNNNN number of each question.
   departments = optional list; when it has items, an optional
   "Your department" picker appears on the home page. */
window.HITS_TRACKING = {
  formAction: '',
  fields: {
    event: '',      // open | task_done | mission_done
    role: '',       // employee | manager
    language: '',   // en | ar
    task: '',       // task or mission id
    score: '',      // points earned for the task (10 or 20)
    session: '',    // random anonymous device code
    department: ''  // optional
  },
  departments: []
};
