def sanitise(example: str, pipelines: list):
    """
    """
    for process in pipelines:
        example = process(example)
    return example
