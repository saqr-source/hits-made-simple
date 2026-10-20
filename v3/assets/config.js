/* HITS Made Simple — optional progress tracking (Google Form).
   mode: 'off'        — nothing is sent (default)
         'anonymous'  — counts opens and finished stops with a random device code
         'workid'     — also asks once for the Work ID so P&C can see who finished.
                        Switch on only after P&C / the director approves; employees see a notice.
   formAction = https://docs.google.com/forms/d/e/<FORM_ID>/formResponse
   fields     = the entry.NNNNNNN number of each question (from the pre-filled link). */
window.HITS_TRACKING = {
  mode: 'off',
  formAction: '',
  fields: {
    event: '',      // open | task_done | mission_done
    role: '',       // employee | manager
    language: '',   // en | ar
    task: '',       // stop or route id
    score: '',      // points earned for the stop (10 or 20)
    session: '',    // random device code
    workId: '',     // only used in 'workid' mode
    department: ''  // optional
  },
  departments: []
};
