
import time
from packages.optimizer.continuous_optimizer import ContinuousOptimizer

def test_continuous_optimizer_runs():
    opt=ContinuousOptimizer()
    opt.start()
    time.sleep(0.15)
    opt.stop()
    time.sleep(0.05)
    assert opt.state.iterations>0
