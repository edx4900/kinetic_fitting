# Kinetic model
def kinetic_model(conc, k2, Kd):
    return k2 * conc / (Kd + conc)

