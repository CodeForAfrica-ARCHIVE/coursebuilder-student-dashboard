# coursebuilder-student-dashboard

This is a Course Builder module which allows students to view and manage their courses and lessons 
in a personalised way. It keeps your lessons organized in one place and also keep track of your progress on each lesson.

The student dashboard is a custom module that was developed as a standalone system i.e 
changes to the course builder codebase was avoided where possible. The module can be integrated 
into the Course builder without breaking anything in the application.

## Requirements

You'll need a system with current versions of `bash` and `git`, as well as
`python` 2.7.

## Getting started

First, clone Course Builder and change directory to the Course Builder root:

```sh
git clone https://github.com/google/coursebuilder-core.git
cd coursebuilder-core/coursebuilder
```

Course Builder provides a management script for fetching modules, so you always
start by grabbing Course Builder, then using it to fetch the module you want to
work with. Let's grab the student dashboard module, called `coursebuilder-student-dashboard`.

Next: run

```
  sh scripts/modules.sh \
    --targets=coursebuilder-student-dashboard@https://github.com/andela-iakande/coursebuilder-student-dashboard.git
```
This script will both download the student dashboard module,install necessary 
dependencies and also link it to Course Builder.

After this process, 
next: Locate the path shown below on your Google Course Builder 

```
  modules/explorer/_static/components/top-bar/top-bar.html 

```
then add the link indicated below into the template tag wherever 
you want your student dashboard link to appear.
         
```
  <a href="/student-dashboard">Student Dashboard</a>

```

For instance you can add it in this template :

```
  <template is="dom-if" if="[[currentUser.loggedIn]]">
  <template>
```  

 Now you can start up Course Builder with the student dashboard module installed:

  ```sh
  sh scripts/start_in_shell.sh
  ```

To view the module in action, visit `localhost:8081/student-dashboard` or visit
localhost:8081, then click on "Student Dashboard".

## Module contents

The structure of this module is

  ```sh
  module.yaml            # Module definition file.
  scripts/
    setup.sh             # Module configuration script.
  src/                   # Module source files.
    static/              # Handles the module's static files
    templates/           # HTML templates.
    student_dashboard.py # Module handler definitions.
    graphql.py           # GraphQL server support for the student dashboard
    top-bar.html         # Component that contain the student dashboard link
  tests/                 # Module tests.
    functional_tests.py  # Example test file.
  ```

### Working from local disk

Sometimes you don't want to fetch a module from a remote repository, but instead
want to use source from local disk. 

We suggest creating a symlink from your local file location to `/tmp/<module>`.
For example, if the code for this module lived in
`/$HOME/src/coursebuilder-student-dashboard/`, you would first create the
symlink by running this:

  ```sh
  ln -s /$HOME/src/coursebuilder-student-dashboard \
      /tmp/coursebuilder-student-dashboard
  ```
After creating the symbolic link, run:

  ```sh
    sh scripts/modules.sh --targets=coursebuilder-student-dashboard@/tmp/
    coursebuilder-student-dashboard
  ```
To install the module from local disk you need to run this script twice 
in order to fetch the module from your coursebuilder resources into your 
application.  

After this process, 
next: Locate the path shown below on your Google Course Builder 

```
  modules/explorer/_static/components/top-bar/top-bar.html

```
then add the link indicated below into the template tag wherever 
you want your student dashboard link to appear.
         
```
  <a href="/student-dashboard">Student Dashboard</a>

```

For instance you can add it in this template as well just as we have done for 
the fetching the module from the remote repository :

```
  <template is="dom-if" if="[[currentUser.loggedIn]]">
  <template>
``` 

 Again, you can start up Course Builder with the student dashboard module installed:

  ```sh
  sh scripts/start_in_shell.sh
  ```

## That's it

Please feel free to integrate this module into your coursebuilder at any time, 
we hope you enjoy using the student-dashboard support for the Course Builder. 


