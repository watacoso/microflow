

# define  possible task states
from enum import Enum

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"

class TaskTriggerRule(Enum):
    ALL_SUCCESS = "all_success"
    ONE_SUCCESS = "all_done"
    ALL_FAILED = "all_failed"
    ONE_FAILED = "one_failed"
    NONE_FAILED = "none_failed"

class BaseTask():
    
    self._task_id = None
    self._task_name = None
    self._task_description = None
    self._task_state = TaskState.PENDING
    self._task_trigger_rule = TaskTriggerRule.ALL_SUCCESS
    
    self._downstream_tasks = []
    self._upstream_tasks = []
    
    
    
    def __init__(self, task_id, task_name, task_description):
        self._task_id = task_id
        self._task_name = task_name
        self._task_description = task_description
        
    @property
    def task_id(self):
        return self._task_id
    
    @property
    def task_name(self):
        return self._task_name
    
    @property
    def task_description(self):
        return self._task_description
    
    
    def __rshift__(self, other):
        if isinstance(other, BaseTask):
            self._downstream_tasks.append(other)
            other._upstream_tasks.append(self)
        return self
    
    
    def run(self):
        """
        Run the task. This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def should_run(self):
        """
        Determine if the task should run based on its state and trigger rule.
        """
        if self._task_state <> TaskState.PENDING:
            return False

        if self._task_trigger_rule == TaskTriggerRule.ALL_SUCCESS:
            return all(task._task_state == TaskState.COMPLETED for task in self._upstream_tasks)
        
        if self._task_trigger_rule == TaskTriggerRule.ONE_SUCCESS:
            return any(task._task_state == TaskState.COMPLETED for task in self._upstream_tasks)
        
        if self._task_trigger_rule == TaskTriggerRule.ALL_FAILED:
            return all(task._task_state == TaskState.FAILED for task in self._upstream_tasks)
        
        if self._task_trigger_rule == TaskTriggerRule.ONE_FAILED:
            return any(task._task_state == TaskState.FAILED for task in self._upstream_tasks)
        
        if self._task_trigger_rule == TaskTriggerRule.NONE_FAILED:
            return all(task._task_state != TaskState.FAILED for task in self._upstream_tasks)
            
    
    def internal_run(self):
        """
        Internal method to run the task. This method should be implemented by subclasses.
        """
        if self.should_run():
            self._task_state = TaskState.RUNNING
            try:
                self.run()
                self._task_state = TaskState.COMPLETED
            except Exception as e:
                self._task_state = TaskState.FAILED
                raise e
            
            ping_downstream_tasks()
        
    def ping_downstream_tasks(self):
        """
        Notify downstream tasks that this task has completed.
        """
        for task in self._downstream_tasks:
            if task.should_run():
                task.internal_run()