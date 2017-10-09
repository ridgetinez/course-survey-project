
### BACKEND DESIGN DECISIONS
* Have a survey controller to handle (well then, technically it's a surveyHandler) all the operations regarding the intermediary between a survey and the flat file storage. This is so that Survey itself would adhere to the S in SOLID + a survey should really know nothing of how it's saved in a flat file - it doesn't need to know that.
* The QuestionStore is a super class yet is also used to capture all the questions that have been made (and not deleted). A survey is just a glorified public QuestionStore, so a Survey inherits from QuestionStore.
* We used dictionaries for quick lookups using qid's as keys. The dictionary initialisation removes all further instances of duplicate questions if there exists that question already in the QuestionStore.
* Favouring lots of aggregation and composition relationships as building blocks for the survey app. At the moment, we don't see the need to absurdly go crazy with multiple inheritances. So with that, we'll be happy suffering a bit more coupling for an easier development experience.
* Writing responses using a CSV file required us to load up the csv into an iterable, find the specific response we want to increment, and then write the whole CSV file again. This is obviously wasteful, but for sake of time, and lack of knowledge, this was the only way we could see this happening.
* Super classes writer and reader there for future iterations. At the moment, not particularly necessary.

### FRONTEND DESIGN DECISIONS
* All templates are designed to have the same theme, most notably the dark navigation bar. Gives off a professional, easy-to-use user interface feel for the admin 
* General flow updated for Iteration 2
  - Landing page (authentication page)
  - 3 different available dashboards: 1 for admin, 1 for staff and 1 for a user
  - Admin must close the survey using a button
* Admin dashboard
  - Mandatory pool and optional pool (iteration 3) of questions
  - Add/delete questions
  - Option to choose date to open/close survey
  - Completed button 
* Staff dashboard
  - Add/delete questions
  - Completed review button
* User dashboard
  - Questions and answers in multiple choice format
  - Completed survey button


### TEAM OPTIMISATION DECISIONS
* Using Slack for communication, LucidCharts for UML drawups, Google Drive for logistic documents, Github for remote git server and tons of coffee.
* Git workflow was to branch out, commit, push changes, pull request, iterate, merge.

