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

Next: create a file titled install.sh. For instance, you can place the file in your desktop and copy the script below into it.

```
  #!/bin/bash
  set -e 
  set -o pipefail
  sh scripts/modules.sh \
    --targets=coursebuilder-student-dashboard@https://github.com/andela-iakande/coursebuilder-student-dashboard.git

  sleep 15 #pause shell script

  cat modules/coursebuilder-student-dashboard/gql.py > modules/gql/gql.py
  cat modules/coursebuilder-student-dashboard/top-bar.html > modules/explorer/_static/components/top-bar/top-bar.html
  rm -f modules/coursebuilder-student-dashboard/gql.py
  rm -f modules/coursebuilder-student-dashboard/top-bar.html
```
After this process, 
next run:

  ```sh
  sh ~/Desktop/install.sh
  ```

This script will both download the student dashboard module, replace some course builder components with appropriate components needed for it to work and also link it to Course Builder.

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
    gql.py               # GraphQL server support for the student dashboard
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

then, create a file titled install.sh. For instance, you can place the file in 
your desktop, copy and paste the script below into it.

  ```
  #!/bin/bash
  set -e 
  set -o pipefail

  cat modules/coursebuilder-student-dashboard/gql.py > modules/gql/gql.py
  cat modules/coursebuilder-student-dashboard/top-bar.html > modules/explorer/_static/components/top-bar/top-bar.html
  rm -f modules/coursebuilder-student-dashboard/gql.py
  rm -f modules/coursebuilder-student-dashboard/top-bar.html
```
from your Course Builder directory, run:
 ```sh
  sh ~/Desktop/install.sh
 ```
When you run this script, it updates your coursebuilder with some
contents required by the student dashboard.
All other scripts then work as above.

## That's it

Please feel free to integrate this module into your coursebuilder at any time, 
we hope you enjoy using the student-dashboard support for the Course Builder. 


