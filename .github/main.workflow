workflow "Build and Test" {
  on = "push"
  resolves = [
    "Test",
  ]
}

action "Build" {
  uses = "jefftriplett/python-actions@master"
  args = "pip install -r requirements.txt && pip install -r requirements_dev.txt && pip install -r requirements_test.txt"
}

action "Lint" {
  uses = "jefftriplett/python-actions@master"
  args = "black --check"
  needs = ["Build"]
}

action "Test" {
  uses = "jefftriplett/python-actions@master"
  args = "pytest"
  needs = ["Lint"]
}