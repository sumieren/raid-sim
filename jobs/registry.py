JOB_REGISTRY = {}

def register_job(job):
    JOB_REGISTRY[job.__name__] = job
    return job