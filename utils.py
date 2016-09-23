def interval_scaler(finterval, tinterval, integers=True):
    scale = (tinterval[1]-tinterval[0]) / (finterval[1]-finterval[0])
    minimum, offset = finterval[0], tinterval[0]
    if integers:
        def scaler(num):
            return round(scale * (num-minimum) + offset)
    else:
        def scaler(num):
            return scale * (num-minimum) + offset
    return scaler