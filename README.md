# miniduct
A python based data orchestration framework with minimal frills, developed for baremetal systems and low batch volumes


steps i am following so far:

sudo apt update
sudo apt install pipx
pipx ensurepath

pipx install poetry

i then created project microflow, added some dependencies. specifically requests, google-cloud-storage,
and for dev pytest, pytest-mock, response 

i also installed gcloud.

---

how should it work?


- microflow starting point is to define a pipeline builder, which is a class that defines the steps in the pipeline
- each step is a class that defines the input and output of the step, as well as the logic of the step
- the pipeline builder will then execute the steps in order, passing the output of each step to the next step

- a single step can trigger multiple steps, which can be defined in the pipeline builder
- the pipeline builder will also handle any dependencies between steps, ensuring that steps are executed in the correct order
- if multiple steps are input to a single step, the pipeline builder will handle merging the outputs of those steps, following the defined logic of the step
- the default is to wait for all input steps to complete before moving on to the next step. 

an example of a step might be:

```
src
|- microflow
    |- steps
        |- BaseStep.py
        |- PythonStep.py
        |- HttpGetStep.py
        |- GCSUploadStep.py
    |- clients
        |- GCSClient.py
        |- HttpClient.py
    |- 
    |- pipeline_builder.py
    |- steps.py
```

```

```python
class FetchDataStep:
    def __init__(self, source):
        self.source = source
    def execute(self):
        # logic to fetch data from the source
        return data

class ProcessDataStep:
    def __init__(self, data):
        self.data = data
    def execute(self):
        # logic to process the data
        return processed_data
```

to connect these steps in a pipeline, you would use the pipeline builder. to concatenate steps, you would contatenate steps like this:

```python
    fetch_data = FetchDataStep(source="https://example.com/data")
    process_data = ProcessDataStep(data=fetch_data.execute())
    fetch_data >> process_data
```
- the `>>` operator is overloaded to allow for easy chaining of steps in the pipeline

```python
class PipelineBuilder:
    def __init__(self):
        self.steps = []
    def add_step(self, step):
        self.steps.append(step)
    def execute(self):
        results = []
        for step in self.steps:
            result = step.execute()
            results.append(result)
        return results
```

here is the overloading system:
```python
class Step:
    def __init__(self):
        self.next_steps = []
    def __rshift__(self, other):
        if isinstance(other, Step):
            self.next_steps.append(other)
            return other
        else:
            raise TypeError("Right operand must be an instance of Step")
    def execute(self):
        result = self.run()
        for next_step in self.next_steps:
            next_step.execute(result)
        return result
    def run(self):
        raise NotImplementedError("Subclasses must implement run method")
```



to do this, the pipeline builder is written this way:


future features:
- the pipeline builder will also handle any errors that occur during the execution of the steps
- the pipeline builder will also handle any retries that are needed for steps that fail
- the pipeline builder will also handle any logging that is needed for the steps
- the pipeline builder will also handle any notifications that are needed for the steps
- the pipeline builder will also handle any caching that is needed for the steps
