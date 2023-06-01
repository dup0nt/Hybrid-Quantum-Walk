from common import Aer

def choose_backend (simulator_variable):
    return Aer.get_backend(simulator_variable)


