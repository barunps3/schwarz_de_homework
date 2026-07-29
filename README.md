# Analysis Pipelines
The notebooks are databricks native but not companion python modules. 
Databricks native objects are not available locally or in CI/CD.
However, functionality of objects in modules can be tested in CI/CD and local machine.

Create and activate your virtual environment before start developing
To build
```
make build
```

To run the test cases. Test cases can only be run on local machine or CI/CD. 
Running test cases in Databricks will fail.
```
make test
```

To fix linting and formatting issues
```
make fix
```