def create_errors_message(problem_name):
    if problem_name == "connection error":
        message = "Please, check Internet connection"
    elif problem_name == "HTTP error":
        message = "You`ve got some problem with HTTP"
    elif problem_name == "permission denied":
        message = "You can not use this directory"
    elif problem_name == "unexpected_err":
        message = "We don`t know, what is wrong"
    elif problem_name == "timeout":
        message = "We are waiting too long"
    print(message)
