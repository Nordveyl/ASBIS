class PID_controller:

    def __init__(self, prop, integr, d):
        self.error_of_pr = 0
        self.error_of_s = 0
        self.prop = prop
        self.integr = integr
        self.d = d

    def evaluation(self, dt, curr, obj):
        error = obj - curr
        self.error_of_s += error
        r = self.prop * error + self.integr * self.error_of_s * dt + self.d * (error - self.error_of_pr) / dt
        self.error_of_pr = error
        return r
