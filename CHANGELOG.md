
### BACKEND DESIGN DECISIONS
* Have a survey controller to handle (well then, technically it's a surveyHandler) all the operations regarding the intermediary between a survey and the flat file storage. This is so that Survey itself would adhere to the S in SOLID + a survey should really know nothing of how it's saved in a flat file - it doesn't need to know that.
* The QuestionStore is a super class yet is also used to capture all the questions that have been made (and not deleted). A survey is just a glorified public QuestionStore, so a Survey inherits from QuestionStore.
* We used dictionaries for quick lookups using qid's as keys. The dictionary initialisation removes all further instances of duplicate questions if there exists that question already in the QuestionStore.
* Favouring lots of aggregation and composition relationships as building blocks for the survey app. At the moment, we don't see the need to absurdly go crazy with multiple inheritances. So with that, we'll be happy suffering a bit more coupling for an easier development experience.

### FRONTEND DESIGN DECISIONS
* All templates are designed to have the same theme, most notably the dark navigation bar. Gives off a professional, easy-to-use user interface feel for the admin 
* General flow for the admin dashboard consists of the landing page (left side - login details, right side - access survey via URL) which directs to the dashboard. In the dashboard there are two main tabs (so far), one for 'create survey' and one for 'create questions'
* Sam decided to set boundaries of the number of answers available for each question (minimum 2 radio buttons, maximum 6 radio buttons)
* Cancel buttons where added to the 'create survey' and 'create questions' form to enhance user experience


### TEAM OPTIMISATION DECISIONS
* Using Slack for communication, LucidCharts for UML drawups, Google Drive for logistic documents, Github for remote git server and tons of coffee.
* Git workflow was to branch out, commit, push changes, pull request, iterate, merge.
* Planning for one diagram per person in the group to understand the challenges from different perspectives (different UML diagram perspectives)
